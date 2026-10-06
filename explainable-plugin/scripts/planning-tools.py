#!/usr/bin/env python3

import argparse
import copy
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tempfile


SAFE_KEY = re.compile(r"[A-Za-z0-9][A-Za-z0-9.-]*\Z")
ID_PATTERNS = {prefix: re.compile(prefix + r"-[A-Z0-9]+-[0-9]{2,}\Z")
               for prefix in ("SCR", "SEC", "CMP", "ELM", "SRC", "DEC")}
TAGS = {"p", "h2", "h3", "button", "input", "textarea", "select", "label", "span"}
STYLES = {
    "flex": "display:flex", "flex-col": "flex-direction:column",
    "grid": "display:grid", "grid-cols-2": "grid-template-columns:repeat(2,minmax(0,1fr))",
    "gap-4": "gap:1rem", "p-4": "padding:1rem", "p-6": "padding:1.5rem",
    "rounded": "border-radius:.25rem", "rounded-lg": "border-radius:.5rem",
    "border": "border:1px solid #cbd5e1", "bg-white": "background:#fff",
    "bg-slate-50": "background:#f8fafc", "bg-blue-600": "background:#2563eb",
    "text-white": "color:#fff", "text-slate-900": "color:#0f172a",
    "text-sm": "font-size:.875rem", "text-xl": "font-size:1.25rem",
    "font-bold": "font-weight:700", "w-full": "width:100%",
}
CAPABILITIES = {"text", "style", "layout", "icons", "badges", "annotations"}
VISUAL_FIELDS = {"label", "classes", "tag", "title"}


def readJson(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def writeJson(path, value, exclusive=False):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if exclusive:
        with target.open("x", encoding="utf-8") as output:
            json.dump(value, output, ensure_ascii=False, indent=2)
            output.write("\n")
        return
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent,
                                     delete=False) as output:
        temporary = Path(output.name)
        json.dump(value, output, ensure_ascii=False, indent=2)
        output.write("\n")
    temporary.replace(target)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safeKey(value):
    if not isinstance(value, str) or not SAFE_KEY.fullmatch(value):
        raise ValueError("버전/스냅샷 키는 영문·숫자·점·하이픈만 허용합니다")
    return value


def paths(domain):
    root = Path(domain)
    return root, root / "planning/state.json", root / "storyboard/annotations.json"


def snapshot(args):
    root = Path(args.domain) / "planning/snapshots" / safeKey(args.id)
    if root.exists():
        raise ValueError("기존 스냅샷은 변경할 수 없습니다")
    materials = readJson(args.materials)
    entries = []
    seenIds = set()
    for material in materials:
        sourceId = material["id"]
        if not ID_PATTERNS["SRC"].fullmatch(sourceId) or sourceId in seenIds:
            raise ValueError("자료 ID가 잘못되었거나 중복입니다: " + sourceId)
        seenIds.add(sourceId)
        for field in ("type", "owner", "origin", "version", "scope", "query", "selection"):
            if field not in material:
                raise ValueError("자료 필드 누락: " + field)
        source = Path(material["path"])
        data = source.read_bytes()
        entry = {key: value for key, value in material.items() if key != "path"}
        entry.update({"file": sourceId + source.suffix.lower(), "sha256": digest(data)})
        entries.append((entry, data))
    root.mkdir(parents=True)
    for entry, data in entries:
        (root / entry["file"]).write_bytes(data)
    writeJson(root / "manifest.json", {"schemaVersion": 1, "id": args.id,
                                      "searchMode": "file-selection",
                                      "materials": [entry for entry, data in entries]}, True)
    print(root / "manifest.json")


def checkSnapshot(root, snapshotId):
    if snapshotId is None:
        return set()
    folder = root / "planning/snapshots" / safeKey(snapshotId)
    manifest = readJson(folder / "manifest.json")
    if manifest.get("schemaVersion") != 1 or manifest.get("id") != snapshotId:
        raise ValueError("스냅샷 manifest 버전/ID 불일치")
    sourceIds = set()
    for material in manifest["materials"]:
        sourceId = material["id"]
        if sourceId in sourceIds or not ID_PATTERNS["SRC"].fullmatch(sourceId):
            raise ValueError("스냅샷 자료 ID 중복/형식 오류")
        sourceIds.add(sourceId)
        filename = material["file"]
        if Path(filename).name != filename:
            raise ValueError("스냅샷 파일은 해당 폴더 내부에 있어야 합니다")
        if digest((folder / filename).read_bytes()) != material["sha256"]:
            raise ValueError("스냅샷 자료 해시 불일치: " + sourceId)
    return sourceIds


def definedIds(root, filename, pattern):
    path = root / "planning" / filename
    if not path.exists():
        return set()
    return set(re.findall(pattern, path.read_text(encoding="utf-8"), re.MULTILINE))


def collectEntities(annotations):
    entities = {}
    for screen in annotations["screens"]:
        for entity in [screen] + screen["sections"] + screen["components"] + screen["elements"]:
            identity = entity["id"]
            if identity in entities:
                raise ValueError("중복 ID: " + identity)
            entities[identity] = entity
    return entities


def validateAnnotations(root, state, annotations, checkDocuments=True):
    if state.get("schemaVersion") != 1 or annotations.get("schemaVersion") != 1:
        raise ValueError("지원하지 않는 schemaVersion")
    safeKey(state["planningVersion"])
    if annotations["planningVersion"] != state["planningVersion"]:
        raise ValueError("기획과 어노테이션 버전 불일치")
    if annotations["snapshotId"] != state["snapshotId"]:
        raise ValueError("기획과 어노테이션 스냅샷 불일치")
    sourceIds = checkSnapshot(root, state["snapshotId"])
    for field in ("screens",):
        if not isinstance(annotations[field], list):
            raise ValueError("어노테이션 목록 형식 오류: " + field)
    for field in ("retiredIds", "decisions", "unresolved", "artifacts"):
        if not isinstance(state[field], list):
            raise ValueError("상태 목록 형식 오류: " + field)
    entities = collectEntities(annotations)
    retiredIds = set(state["retiredIds"])
    if retiredIds & entities.keys():
        raise ValueError("폐기 ID를 재사용했습니다")
    screenIds = {screen["id"] for screen in annotations["screens"]}
    storyIds = definedIds(root, "user-stories.md", r"^#{2,4} (US-[0-9]+)\b")
    requirementIds = definedIds(root, "requirements.md", r"^#{2,4} ((?:FR|NFR)-[A-Z0-9-]+)\b")
    flowIds = definedIds(root, "user-flows.md", r"^#{2,4} (UF-[a-z0-9-]+)\b")
    iaIds = definedIds(root, "information-architecture.md", r"^\| *(SCR-[A-Z0-9-]+)\b")
    specPath = root / "planning/screen-spec.md"
    if annotations["screens"] and checkDocuments:
        if iaIds != screenIds:
            raise ValueError("IA와 어노테이션 화면 집합 불일치")
        if not specPath.exists():
            raise ValueError("화면 기능정의서가 없습니다")
        specContent = specPath.read_text(encoding="utf-8")
        versions = re.findall(r"^\| *기획 버전 *\| *([^|]+?) *\|", specContent, re.MULTILINE)
        if versions != [state["planningVersion"]]:
            raise ValueError("화면 기능정의서의 기획 버전 불일치")
        specIds = set(re.findall(r"\b(?:SCR|SEC|CMP|ELM)-[A-Z0-9]+-[0-9]{2,}\b",
                                specContent))
        if specIds != entities.keys():
            raise ValueError("기능정의서와 어노테이션 ID 불일치")
    for screen in annotations["screens"]:
        for field in ("storyIds", "flowIds", "sections", "components", "elements"):
            if not isinstance(screen[field], list):
                raise ValueError("화면 목록 형식 오류: " + field)
        if not isinstance(screen["title"], str) or not screen["title"].strip():
            raise ValueError("화면 제목 누락")
        if not ID_PATTERNS["SCR"].fullmatch(screen["id"]):
            raise ValueError("잘못된 화면 ID")
        if screen["kind"] not in {"page", "overlay", "state"}:
            raise ValueError("잘못된 화면 유형")
        if screen["kind"] == "page":
            if screen["parentScreenId"] is not None:
                raise ValueError("page는 부모 화면을 가지지 않습니다")
        elif screen["parentScreenId"] not in screenIds or not any(
                parent["id"] == screen["parentScreenId"] and parent["kind"] == "page"
                for parent in annotations["screens"]):
            raise ValueError("overlay/state 부모 화면 참조 오류")
        if not screen["storyIds"] or not screen["flowIds"]:
            raise ValueError("화면의 스토리/플로우 연결이 없습니다")
        if not set(screen["storyIds"]) <= storyIds or not set(screen["flowIds"]) <= flowIds:
            raise ValueError("화면의 스토리/플로우 참조 오류")
        sections = {section["id"] for section in screen["sections"]}
        components = {component["id"]: component for component in screen["components"]}
        for section in screen["sections"]:
            if not ID_PATTERNS["SEC"].fullmatch(section["id"]) or not section["title"]:
                raise ValueError("섹션 형식 오류")
        for component in screen["components"]:
            if not ID_PATTERNS["CMP"].fullmatch(component["id"]) or component["sectionId"] not in sections:
                raise ValueError("컴포넌트 형식/섹션 참조 오류")
        badges = set()
        for element in screen["elements"]:
            for field in ("classes", "states", "requirementIds", "sourceIds"):
                if not isinstance(element[field], list):
                    raise ValueError("요소 목록 형식 오류: " + field)
            if not ID_PATTERNS["ELM"].fullmatch(element["id"]):
                raise ValueError("잘못된 요소 ID")
            if element["sectionId"] not in sections or element["componentId"] not in components:
                raise ValueError("요소의 섹션/컴포넌트 참조 오류")
            if components[element["componentId"]]["sectionId"] != element["sectionId"]:
                raise ValueError("요소와 컴포넌트의 섹션 불일치")
            badge = element["badge"]
            if type(badge) is not int or badge < 1 or badge in badges:
                raise ValueError("배지 번호 형식 오류/중복")
            badges.add(badge)
            if element["tag"] not in TAGS or not set(element["classes"]) <= STYLES.keys():
                raise ValueError("미지원 HTML tag/class")
            for field in ("label", "description", "action", "validation", "permission"):
                if not isinstance(element[field], str) or not element[field].strip():
                    raise ValueError("요소 설명 누락: " + field)
            if not element["states"] or not all(isinstance(value, str) for value in element["states"]):
                raise ValueError("요소 상태 누락")
            if not element["requirementIds"] or not set(element["requirementIds"]) <= requirementIds:
                raise ValueError("요소 요구사항 참조 오류")
            if not set(element["sourceIds"]) <= sourceIds:
                raise ValueError("요소 자료 근거 참조 오류")
            if element["figmaNodeId"] is not None and not isinstance(element["figmaNodeId"], str):
                raise ValueError("잘못된 Figma 노드 ID")
    for decision in state["decisions"]:
        if not ID_PATTERNS["DEC"].fullmatch(decision["id"]):
            raise ValueError("잘못된 결정 ID")
        if decision["status"] not in {"pending", "accepted", "rejected", "superseded"}:
            raise ValueError("잘못된 결정 상태")
        if not isinstance(decision["value"], str) or not decision["value"].strip():
            raise ValueError("결정 내용 누락")
        decisionSources = checkSnapshot(root, decision.get("snapshotId", state["snapshotId"]))
        if not set(decision["sourceIds"]) <= decisionSources:
            raise ValueError("결정 자료 근거 참조 오류")
        if not set(decision["screenIds"]) <= screenIds | retiredIds:
            raise ValueError("결정 화면 참조 오류")
    if len({decision["id"] for decision in state["decisions"]}) != len(state["decisions"]):
        raise ValueError("중복 결정 ID")
    for oldId, newIds in state["replacements"].items():
        if oldId not in retiredIds or not set(newIds) <= entities.keys():
            raise ValueError("대체 ID 관계 오류")


class StoryboardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []
        self.rows = []
        self.version = None
        self.unsafe = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag in {"script", "iframe", "object", "embed"} or any(key.startswith("on") for key in values):
            self.unsafe = True
        if tag == "meta" and values.get("name") == "planning-version":
            self.version = values.get("content")
        if "data-element-id" in values:
            self.elements.append((values["data-element-id"], values.get("data-badge")))
        if "data-description-for" in values:
            self.rows.append((values["data-description-for"], values.get("data-badge")))


def checkDomain(domain, requireHtml=False, checkDesignInputs=True):
    root, statePath, annotationsPath = paths(domain)
    if not statePath.exists():
        if annotationsPath.exists():
            raise ValueError("어노테이션에 대응하는 state.json이 없습니다")
        return
    state = readJson(statePath)
    if state["mode"] not in {"forward", "reverse"}:
        raise ValueError("잘못된 생성 모드")
    if state["status"] not in {"draft", "in-review", "changes-requested", "approved"}:
        raise ValueError("잘못된 검토 상태")
    if state["status"] == "approved" and (state["approvedVersion"] != state["planningVersion"]
                                         or state["unresolved"] or not state["reviewer"]):
        raise ValueError("승인 버전/미결/검토자 불일치")
    if checkDesignInputs and state.get("designReadyVersion") is not None:
        if state["designReadyVersion"] != state["planningVersion"] or state["status"] != "approved":
            raise ValueError("개발 설계 준비 버전 불일치")
        if not state.get("designInputs"):
            raise ValueError("개발 설계 입력 누락")
        for relative, expected in state["designInputs"].items():
            target = (root / relative).resolve()
            if not target.is_relative_to(root.parent.resolve()) or digest(target.read_bytes()) != expected:
                raise ValueError("개발 설계 입력 변경: " + relative)
    annotations = readJson(annotationsPath)
    validateAnnotations(root, state, annotations)
    artifacts = {artifact["path"]: artifact for artifact in state["artifacts"]}
    for screen in annotations["screens"]:
        relative = "storyboard/" + screen["id"] + ".html"
        target = root / relative
        if not target.exists():
            if requireHtml:
                raise ValueError("목업 누락: " + relative)
            continue
        artifact = artifacts.get(relative)
        if artifact and artifact["status"] == "stale":
            if requireHtml:
                raise ValueError("갱신 필요한 목업: " + relative)
            continue
        parser = StoryboardParser()
        parser.feed(target.read_text(encoding="utf-8"))
        expected = sorted((element["id"], str(element["badge"])) for element in screen["elements"])
        expectedVersion = artifact["planningVersion"] if artifact else state["planningVersion"]
        if parser.unsafe or parser.version != expectedVersion:
            raise ValueError("목업 실행 요소 또는 버전 불일치")
        if sorted(parser.elements) != expected or sorted(parser.rows) != expected:
            raise ValueError("배지·설명 패널 누락/중복/고아 참조: " + relative)
    for artifact in state["artifacts"]:
        if artifact["status"] not in {"current", "stale"}:
            raise ValueError("잘못된 파생물 상태")
        if artifact["status"] == "current" and artifact.get("verifiedForVersion", artifact["planningVersion"]) != state["planningVersion"]:
            raise ValueError("파생물 기준 버전 불일치")
        target = (root / artifact["path"]).resolve()
        if not target.is_relative_to(root.resolve()):
            raise ValueError("파생물 경로가 도메인 밖입니다")
        if artifact["status"] == "current" and not target.exists():
            raise ValueError("파생물 파일 누락")
        if artifact["status"] == "current" and artifact.get("sha256") and digest(target.read_bytes()) != artifact["sha256"]:
            raise ValueError("파생물에 반영되지 않은 수동 수정이 있습니다: " + artifact["path"])


def checkTree(root):
    root = Path(root)
    domains = {path.parent.parent for pattern in ("planning/state.json", "storyboard/annotations.json")
               for path in root.rglob(pattern)
               if not {"revisions", "snapshots"} & set(path.relative_to(root).parts)}
    for domain in sorted(domains):
        checkDomain(domain)


def classifyDocument(path):
    path = Path(path)
    content = path.read_text(encoding="utf-8")
    evidence = []
    statePath = path.parent / "state.json"
    if statePath.exists():
        evidence.append(readJson(statePath).get("mode"))
    markers = re.findall(r"<!-- GENERATED-BY: (.*?) -->", content, re.DOTALL)
    for marker in markers:
        explicit = re.search(r"\bmode: (forward|reverse)\b", marker)
        inferred = ("forward" if marker.startswith("init-") else
                    "reverse" if marker.startswith("reverse-") else None)
        if explicit:
            evidence.append(explicit.group(1))
        if inferred:
            evidence.append(inferred)
    if not evidence and "## 읽은 소스" in content and re.search(r"\[REF: [^\]]+:[0-9]+\]", content):
        evidence.append("reverse")
    valid = {mode for mode in evidence if mode in {"forward", "reverse"}}
    mode = next(iter(valid)) if len(valid) == 1 and all(item in valid for item in evidence) else None
    return {"mode": mode, "evidence": evidence, "requiresReview": mode is None,
            "deletionAuthorized": False}


def freezeDomain(domain):
    root, statePath, annotationsPath = paths(domain)
    state = readJson(statePath)
    target = root / "planning/revisions" / safeKey(state["planningVersion"])
    files = list((root / "planning").glob("*.md")) + [statePath, annotationsPath]
    records = {str(path.relative_to(root)): path.read_bytes() for path in files}
    manifest = {name: digest(data) for name, data in records.items()}
    if target.exists():
        stored = readJson(target / "manifest.json")
        if stored != manifest or any(digest((target / name).read_bytes()) != value
                                      for name, value in stored.items()):
            raise ValueError("동일 버전의 보관본과 내용이 다릅니다. 새 버전을 부여하세요")
        return
    for name, data in records.items():
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    writeJson(target / "manifest.json", manifest, True)


def revise(args):
    root, statePath, annotationsPath = paths(args.domain)
    checkDomain(root, checkDesignInputs=False)
    state = readJson(statePath)
    previous = readJson(annotationsPath)
    candidate = readJson(args.candidate)
    safeKey(args.version)
    if args.version == state["planningVersion"] or (root / "planning/revisions" / args.version).exists():
        raise ValueError("수정에는 새 버전이 필요합니다")
    oldScreens = {screen["id"]: screen for screen in previous["screens"]}
    newScreens = {screen["id"]: screen for screen in candidate["screens"]}
    if args.mode != "restructure" and oldScreens.keys() != newScreens.keys():
        raise ValueError("이 수정 모드는 화면 집합을 보존해야 합니다")
    if args.mode == "screen":
        if args.screen not in oldScreens:
            raise ValueError("수정 대상 화면이 없습니다")
        if any(value != newScreens[identity] for identity, value in oldScreens.items() if identity != args.screen):
            raise ValueError("단일 화면 수정에서 다른 화면을 변경했습니다")
    if args.mode == "references":
        if candidate["snapshotId"] == state["snapshotId"] or candidate["snapshotId"] is None:
            raise ValueError("자료 재선택에는 새 스냅샷이 필요합니다")
    elif candidate["snapshotId"] != state["snapshotId"]:
        raise ValueError("자료 변경은 references 모드에서 수행하세요")
    updated = copy.deepcopy(state)
    removedIds = collectEntities(previous).keys() - collectEntities(candidate).keys()
    updated["retiredIds"] = sorted(set(state["retiredIds"]) | removedIds)
    updated.update({"planningVersion": args.version, "snapshotId": candidate["snapshotId"],
                    "status": "changes-requested", "approvedVersion": None, "reviewer": None,
                    "designReadyVersion": None, "designInputs": {}})
    if args.mode == "references":
        for decision in updated["decisions"]:
            decision.setdefault("snapshotId", state["snapshotId"])
    if args.replacements:
        updated["replacements"].update(readJson(args.replacements))
    updated["lastChange"] = {"mode": args.mode, "screenId": args.screen, "reason": args.reason,
                             "previousVersion": state["planningVersion"]}
    changedScreens = oldScreens.keys() | newScreens.keys() if args.mode == "references" else {
        identity for identity in oldScreens.keys() | newScreens.keys()
        if oldScreens.get(identity) != newScreens.get(identity)}
    for artifact in updated["artifacts"]:
        scope = set(artifact.get("screenIds", []))
        if artifact["status"] == "current" and scope and not scope & changedScreens:
            artifact["verifiedForVersion"] = args.version
        else:
            artifact["status"] = "stale"
    validateAnnotations(root, updated, candidate, False)
    freezeDomain(root)
    writeJson(annotationsPath, candidate)
    writeJson(statePath, updated)
    print("수정된 화면 기능정의·IA·플로우·추적성 대응을 확인하세요")


def renderScreen(screen, version):
    escape = html.escape
    css = "\n".join("." + name + "{" + value + "}" for name, value in STYLES.items())
    blocks = []
    for section in screen["sections"]:
        content = ["<section class='p-4 border rounded-lg'><h2>" + escape(section["title"]) + "</h2>"]
        for component in screen["components"]:
            if component["sectionId"] != section["id"]:
                continue
            content.append("<div class='flex flex-col gap-4'><h3>" + escape(component["title"]) + "</h3>")
            for element in screen["elements"]:
                if element["componentId"] != component["id"]:
                    continue
                identity, badge = escape(element["id"]), str(element["badge"])
                label, tag = escape(element["label"]), element["tag"]
                attributes = " class='" + escape(" ".join(element["classes"])) + "' aria-label='" + label + "'"
                if tag == "input":
                    control = "<input" + attributes + " placeholder='" + label + "'>"
                elif tag == "select":
                    control = "<select" + attributes + "><option>" + label + "</option></select>"
                else:
                    if tag == "button":
                        attributes += " type='button'"
                    control = "<" + tag + attributes + ">" + label + "</" + tag + ">"
                content.append("<div data-element-id='" + identity + "' data-badge='" + badge + "'>"
                               "<span class='badge'>" + badge + "</span>" + control + "</div>")
            content.append("</div>")
        content.append("</section>")
        blocks.append("\n".join(content))
    rows = []
    for element in screen["elements"]:
        description = " · ".join([element["description"], element["action"], element["validation"],
                                   element["permission"], ", ".join(element["states"]),
                                   ", ".join(element["requirementIds"] + element["sourceIds"])])
        rows.append("<tr data-description-for='" + escape(element["id"]) + "' data-badge='"
                    + str(element["badge"]) + "'><td>" + str(element["badge"]) + "</td><td>"
                    + escape(element["id"]) + "</td><td>" + escape(description) + "</td></tr>")
    return ("<!doctype html><html lang='ko'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<meta name='planning-version' content='" + escape(version) + "'>"
            "<meta http-equiv='Content-Security-Policy' content=\"default-src 'none'; style-src 'unsafe-inline'\">"
            "<title>" + escape(screen["title"]) + "</title><style>" + css
            + "\n*{box-sizing:border-box}body{font-family:system-ui;margin:0;padding:1rem;background:#f8fafc}"
            "main{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);gap:1rem}"
            "article{display:flex;flex-direction:column;gap:1rem}article,aside{min-width:0}"
            "table{border-collapse:collapse;width:100%;table-layout:fixed}"
            "th:first-child{width:3rem}th:nth-child(2){width:7rem}"
            "td,th{padding:.5rem;border:1px solid #cbd5e1;overflow-wrap:anywhere}"
            ".badge{display:inline-block;background:#0f172a;color:white;padding:.2rem .45rem;"
            "border-radius:1rem;margin-right:.5rem;vertical-align:top}input,textarea,select{max-width:100%}"
            "@media(max-width:768px){main{grid-template-columns:minmax(0,1fr)}}"
            "</style></head><body><h1>" + escape(screen["title"]) + "</h1><main><article>"
            + "\n".join(blocks) + "</article><aside><h2>기능 설명</h2><table><thead><tr>"
            "<th>배지</th><th>요소</th><th>설명·동작·검증·권한·상태·근거</th></tr></thead><tbody>"
            + "\n".join(rows) + "</tbody></table></aside></main></body></html>\n")


def restore(args):
    root, statePath, annotationsPath = paths(args.domain)
    checkDomain(root, checkDesignInputs=False)
    currentState, currentAnnotations = readJson(statePath), readJson(annotationsPath)
    archive = root / "planning/revisions" / safeKey(args.from_version)
    safeKey(args.version)
    if args.version == currentState["planningVersion"] or (root / "planning/revisions" / args.version).exists():
        raise ValueError("복원에는 새 버전이 필요합니다")
    manifest = readJson(archive / "manifest.json")
    for relative, expected in manifest.items():
        target = (archive / relative).resolve()
        if not target.is_relative_to(archive.resolve()) or digest(target.read_bytes()) != expected:
            raise ValueError("복원 보관본 해시/경로 오류")
    restoredState = readJson(archive / "planning/state.json")
    restoredAnnotations = readJson(archive / "storyboard/annotations.json")
    restoredIds = collectEntities(restoredAnnotations).keys()
    removed = collectEntities(currentAnnotations).keys() - restoredIds
    restoredState["retiredIds"] = sorted((set(currentState["retiredIds"]) |
                                          set(restoredState["retiredIds"]) | removed) - restoredIds)
    decisions = {decision["id"]: dict(decision, snapshotId=decision.get("snapshotId", restoredState["snapshotId"]))
                 for decision in restoredState["decisions"]}
    for decision in currentState["decisions"]:
        decisions[decision["id"]] = dict(decision, snapshotId=decision.get("snapshotId", currentState["snapshotId"]))
    restoredState["decisions"] = list(decisions.values())
    restoredState["unresolved"] = list(dict.fromkeys(restoredState["unresolved"] + currentState["unresolved"]))
    restoredState["replacements"] = {identity: replacements for identity, replacements in restoredState["replacements"].items()
                                     if identity in restoredState["retiredIds"] and set(replacements) <= restoredIds}
    restoredState.update({"planningVersion": args.version, "status": "changes-requested",
                          "approvedVersion": None, "reviewer": None, "designReadyVersion": None,
                          "designInputs": {}, "lastChange": {"mode": "restore", "reason": args.reason,
                          "fromVersion": args.from_version, "previousVersion": currentState["planningVersion"]}})
    restoredAnnotations["planningVersion"] = args.version
    for artifact in restoredState["artifacts"]:
        artifact["status"] = "stale"
    validateAnnotations(root, restoredState, restoredAnnotations, False)
    freezeDomain(root)
    for relative in manifest:
        if relative.startswith("planning/") and relative.endswith(".md"):
            content = (archive / relative).read_text(encoding="utf-8")
            content = re.sub(r"(^\| *기획 버전 *\| *)[^|]+( *\|)",
                             lambda match: match.group(1) + args.version + match.group(2), content, flags=re.MULTILINE)
            (root / relative).write_text(content, encoding="utf-8")
    writeJson(annotationsPath, restoredAnnotations)
    writeJson(statePath, restoredState)
    print("이전 기획을 새 검토 버전으로 복원했습니다. 최신 결정과 문서 의미를 확인하세요")


def build(args):
    root, statePath, annotationsPath = paths(args.domain)
    checkDomain(root)
    state = readJson(statePath)
    if state["status"] != "approved":
        raise ValueError("승인된 기획만 목업을 생성할 수 있습니다")
    annotations = readJson(annotationsPath)
    artifacts = {artifact["path"]: artifact for artifact in state["artifacts"]}
    for screen in annotations["screens"]:
        relative = "storyboard/" + screen["id"] + ".html"
        existing = artifacts.get(relative)
        target = root / relative
        if target.exists() and (not existing or digest(target.read_bytes()) != existing.get("sha256")):
            raise ValueError("목업에 보존할 수동 수정이 있습니다: " + relative)
    for screen in annotations["screens"]:
        relative = "storyboard/" + screen["id"] + ".html"
        existing = artifacts.get(relative)
        if existing and existing["status"] == "current" and existing.get(
                "verifiedForVersion", existing["planningVersion"]) == state["planningVersion"]:
            continue
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(renderScreen(screen, state["planningVersion"]), encoding="utf-8")
        artifacts[relative] = {"kind": "html", "path": relative, "planningVersion": state["planningVersion"],
                               "status": "current", "sha256": digest(target.read_bytes()), "screenIds": [screen["id"]]}
    state["artifacts"] = list(artifacts.values())
    writeJson(statePath, state)
    checkDomain(root, True)
    print("목업 생성·배지 대응 검사 통과")


def approve(args):
    root, statePath, annotationsPath = paths(args.domain)
    checkDomain(root)
    state = readJson(statePath)
    if args.version != state["planningVersion"] or state["unresolved"] or not args.reviewer.strip():
        raise ValueError("승인 버전/미결 사항/검토자를 확인하세요")
    if any(decision["status"] == "pending" for decision in state["decisions"]):
        raise ValueError("미결 결정이 남아 있습니다")
    state.update({"status": "approved", "approvedVersion": args.version, "reviewer": args.reviewer})
    writeJson(statePath, state)
    print("승인 버전: " + args.version)


def exportSync(args):
    root, statePath, annotationsPath = paths(args.domain)
    checkDomain(root, True)
    state = readJson(statePath)
    if state["status"] != "approved":
        raise ValueError("승인된 버전만 디자인 교환 가능합니다")
    package = {"schemaVersion": 1, "baseVersion": state["planningVersion"],
               "figmaFileId": args.figma_file, "annotations": readJson(annotationsPath),
               "capabilities": {name: name != "icons" for name in sorted(CAPABILITIES)},
               "losses": ["아이콘은 텍스트 대체이며 원본 SVG 왕복을 지원하지 않습니다"],
               "htmlHashes": {artifact["path"]: digest((root / artifact["path"]).read_bytes())
                              for artifact in state["artifacts"] if artifact["kind"] == "html"
                              and artifact["status"] == "current"},
               "artifactVersions": {artifact["path"]: {"generatedFrom": artifact["planningVersion"],
                                    "verifiedFor": artifact.get("verifiedForVersion", artifact["planningVersion"])}
                                    for artifact in state["artifacts"] if artifact["status"] == "current"}}
    writeJson(args.output, package, True)
    print(args.output)


def readyDesign(args):
    root, statePath, annotationsPath = paths(args.domain)
    checkDomain(root, checkDesignInputs=False)
    state = readJson(statePath)
    if state["status"] != "approved" or args.version != state["planningVersion"]:
        raise ValueError("개발 설계 준비는 승인된 정확한 기획 버전이 필요합니다")
    inputs = ["../architecture.md", "../infrastructure.md", "planning/api-interface.md"]
    state["designInputs"] = {relative: digest((root / relative).read_bytes()) for relative in inputs}
    state["designReadyVersion"] = args.version
    writeJson(statePath, state)
    print("개발 설계 준비 버전: " + args.version)


def flatten(annotations):
    entities = collectEntities(annotations)
    result = {}
    for screen in annotations["screens"]:
        result[screen["id"]] = {key: value for key, value in screen.items()
                                if key not in {"sections", "components", "elements"}}
        for group in ("sections", "components", "elements"):
            for entity in screen[group]:
                result[entity["id"]] = dict(entity, screenId=screen["id"])
    if result.keys() != entities.keys():
        raise ValueError("디자인 엔티티 대응 오류")
    return result


def compareSync(args):
    root, statePath, annotationsPath = paths(args.domain)
    checkDomain(root)
    baseline, incoming = readJson(args.baseline), readJson(args.incoming)
    if baseline.get("schemaVersion") != 1 or incoming.get("schemaVersion") != 1:
        raise ValueError("디자인 교환 schemaVersion 오류")
    if incoming["baseVersion"] != baseline["baseVersion"]:
        raise ValueError("동기화 기준 버전 불일치")
    if not baseline["figmaFileId"] or incoming["figmaFileId"] != baseline["figmaFileId"]:
        raise ValueError("Figma 파일 매핑 누락/불일치")
    if baseline["annotations"]["planningVersion"] != baseline["baseVersion"]:
        raise ValueError("기준 패키지 버전 오류")
    original = flatten(baseline["annotations"])
    current = flatten(readJson(annotationsPath))
    external = flatten(incoming["annotations"])
    changes, conflicts = [], []
    for identity in sorted(original.keys() | current.keys() | external.keys()):
        before, local, remote = original.get(identity), current.get(identity), external.get(identity)
        if remote == before:
            continue
        if before is None or remote is None:
            change = {"id": identity, "field": "entity", "kind": "structure",
                      "before": before, "current": local, "incoming": remote}
            (conflicts if local != before and local != remote else changes).append(change)
            continue
        if local is None:
            conflicts.append({"id": identity, "field": "entity", "kind": "structure",
                              "before": before, "current": None, "incoming": remote})
            continue
        for field in sorted(before.keys() | remote.keys()):
            oldValue, localValue, remoteValue = before.get(field), local.get(field), remote.get(field)
            if oldValue == remoteValue:
                continue
            change = {"id": identity, "field": field,
                      "kind": "visual" if field in VISUAL_FIELDS else "functional",
                      "before": oldValue, "current": localValue, "incoming": remoteValue}
            (conflicts if localValue != oldValue and localValue != remoteValue else changes).append(change)
    losses = list(baseline["losses"]) + list(incoming["losses"])
    candidateState = copy.deepcopy(readJson(statePath))
    candidateState.update({"planningVersion": incoming["annotations"]["planningVersion"],
                           "snapshotId": incoming["annotations"]["snapshotId"]})
    try:
        validateAnnotations(root, candidateState, incoming["annotations"], False)
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as error:
        losses.append("가져온 화면 계약 오류: " + str(error))
    nodes = []
    for screen in incoming["annotations"]["screens"]:
        for element in screen["elements"]:
            if not element.get("figmaNodeId"):
                losses.append("Figma 요소 매핑 누락: " + element["id"])
            else:
                nodes.append(element["figmaNodeId"])
    if len(nodes) != len(set(nodes)):
        losses.append("Figma 노드 매핑 중복")
    unsupported = sorted(name for name in CAPABILITIES
                         if incoming["capabilities"].get(name) is not True)
    report = {"schemaVersion": 1, "baseVersion": baseline["baseVersion"],
              "currentVersion": readJson(statePath)["planningVersion"], "changes": changes,
              "conflicts": conflicts, "losses": sorted(set(losses)), "unsupported": unsupported,
              "ready": not conflicts and not losses and not unsupported,
              "applied": False}
    writeJson(args.output, report, True)
    print(args.output)


def main():
    parser = argparse.ArgumentParser(description="자료 스냅샷·기획 수정·목업·디자인 변경 검토")
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("snapshot")
    command.add_argument("domain")
    command.add_argument("materials")
    command.add_argument("--id", required=True)
    command.set_defaults(run=snapshot)
    command = commands.add_parser("check")
    command.add_argument("domain")
    command.add_argument("--require-html", action="store_true")
    command.set_defaults(run=lambda args: checkDomain(args.domain, args.require_html))
    command = commands.add_parser("check-tree")
    command.add_argument("root")
    command.set_defaults(run=lambda args: checkTree(args.root))
    command = commands.add_parser("classify")
    command.add_argument("document")
    command.set_defaults(run=lambda args: print(json.dumps(classifyDocument(args.document), ensure_ascii=False)))
    command = commands.add_parser("freeze")
    command.add_argument("domain")
    command.set_defaults(run=lambda args: freezeDomain(args.domain))
    command = commands.add_parser("revise")
    command.add_argument("domain")
    command.add_argument("candidate")
    command.add_argument("--mode", choices=["screen", "preserve", "restructure", "references"], required=True)
    command.add_argument("--screen")
    command.add_argument("--version", required=True)
    command.add_argument("--reason", required=True)
    command.add_argument("--replacements")
    command.set_defaults(run=revise)
    command = commands.add_parser("approve")
    command.add_argument("domain")
    command.add_argument("--version", required=True)
    command.add_argument("--reviewer", required=True)
    command.set_defaults(run=approve)
    command = commands.add_parser("restore")
    command.add_argument("domain")
    command.add_argument("--from-version", required=True)
    command.add_argument("--version", required=True)
    command.add_argument("--reason", required=True)
    command.set_defaults(run=restore)
    command = commands.add_parser("build")
    command.add_argument("domain")
    command.set_defaults(run=build)
    command = commands.add_parser("ready-design")
    command.add_argument("domain")
    command.add_argument("--version", required=True)
    command.set_defaults(run=readyDesign)
    command = commands.add_parser("export-sync")
    command.add_argument("domain")
    command.add_argument("--figma-file", required=True)
    command.add_argument("--output", required=True)
    command.set_defaults(run=exportSync)
    command = commands.add_parser("compare-sync")
    command.add_argument("domain")
    command.add_argument("baseline")
    command.add_argument("incoming")
    command.add_argument("--output", required=True)
    command.set_defaults(run=compareSync)
    args = parser.parse_args()
    try:
        args.run(args)
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as error:
        print("오류: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
