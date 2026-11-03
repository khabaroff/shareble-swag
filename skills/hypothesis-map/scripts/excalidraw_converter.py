"""
Конвертер карты гипотез в формат Excalidraw.

Создаёт горизонтальную раскладку: Цель → Субъекты → Гипотезы → Задачи
Текст привязан к прямоугольникам через containerId/boundElements.
"""

import json
import random
from typing import Dict, List, Any, Tuple

try:
    from .model import HypothesisMap, Goal, Subject, Hypothesis, Task, Metric, Priority
except ImportError:
    from model import HypothesisMap, Goal, Subject, Hypothesis, Task, Metric, Priority


# Цвета элементов (HEX)
COLORS = {
    "goal": "#cadf58",
    "subject": "#ffc831",
    "hypothesis": "#ffef73",
    "task": "#a6cdff",
    "stroke": "#1e1e1e",
}

# Цвета приоритетов для стрелок
PRIORITY_COLORS = {
    Priority.HIGH: "#FF7373",
    Priority.MEDIUM: "#FFC831",
    Priority.LOW: "#8FD14F",
    Priority.NONE: "#70736d",
}

# Толщина стрелок по приоритету
PRIORITY_STROKE = {
    Priority.HIGH: 4,
    Priority.MEDIUM: 3,
    Priority.LOW: 2,
    Priority.NONE: 2,
}


def generate_id() -> str:
    """Генерирует уникальный ID."""
    return f"{random.randint(100000, 999999)}"


def wrap_text(text: str, max_chars_per_line: int = 30) -> str:
    """
    Переносит текст по словам, чтобы строки не превышали max_chars_per_line.
    Сохраняет существующие переносы строк.
    """
    lines = text.split('\n')
    wrapped_lines = []

    for line in lines:
        if len(line) <= max_chars_per_line:
            wrapped_lines.append(line)
        else:
            words = line.split(' ')
            current_line = ""
            for word in words:
                if not current_line:
                    current_line = word
                elif len(current_line) + 1 + len(word) <= max_chars_per_line:
                    current_line += " " + word
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
            if current_line:
                wrapped_lines.append(current_line)

    return '\n'.join(wrapped_lines)


def generate_seed() -> int:
    """Генерирует seed для Excalidraw."""
    return random.randint(100000000, 999999999)


def create_card(
    card_id: str,
    text_id: str,
    x: float,
    y: float,
    width: float,
    height: float,
    bg_color: str,
    text: str,
    font_size: int = 14
) -> Tuple[Dict, Dict]:
    """
    Создаёт карточку (прямоугольник + текст внутри).

    Returns:
        Кортеж (rectangle_element, text_element)
    """
    # Оценка высоты текста
    lines = text.count('\n') + 1
    text_height = lines * font_size * 1.25

    # Прямоугольник
    rect = {
        "id": card_id,
        "type": "rectangle",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeColor": COLORS["stroke"],
        "backgroundColor": bg_color,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 3},
        "seed": generate_seed(),
        "version": 1,
        "versionNonce": generate_seed(),
        "isDeleted": False,
        "boundElements": [{"id": text_id, "type": "text"}],
        "updated": 1,
        "link": None,
        "locked": False
    }

    # Текст (привязан к прямоугольнику) — центрирован по вертикали
    text_elem = {
        "id": text_id,
        "type": "text",
        "x": x + 10,
        "y": y + (height - text_height) / 2,
        "width": width - 20,
        "height": text_height,
        "angle": 0,
        "strokeColor": COLORS["stroke"],
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": generate_seed(),
        "version": 1,
        "versionNonce": generate_seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": font_size,
        "fontFamily": 3,  # Monospace
        "textAlign": "left",
        "verticalAlign": "middle",
        "containerId": card_id,
        "originalText": text,
        "lineHeight": 1.25
    }

    return rect, text_elem


def create_arrow(
    arrow_id: str,
    start_id: str,
    end_id: str,
    start_x: float,
    start_y: float,
    end_x: float,
    end_y: float,
    color: str,
    stroke_width: int = 2
) -> Dict:
    """Создаёт стрелку между элементами."""
    return {
        "id": arrow_id,
        "type": "arrow",
        "x": start_x,
        "y": start_y,
        "width": abs(end_x - start_x),
        "height": abs(end_y - start_y),
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": stroke_width,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "seed": generate_seed(),
        "version": 1,
        "versionNonce": generate_seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "points": [[0, 0], [end_x - start_x, end_y - start_y]],
        "lastCommittedPoint": None,
        "startBinding": {
            "elementId": start_id,
            "focus": 0,
            "gap": 5
        },
        "endBinding": {
            "elementId": end_id,
            "focus": 0,
            "gap": 5
        },
        "startArrowhead": None,
        "endArrowhead": "arrow"
    }


def create_label(text: str, x: float, y: float, width: float) -> Dict:
    """Создаёт заголовок колонки."""
    label_id = f"label-{generate_id()}"
    return {
        "id": label_id,
        "type": "text",
        "x": x,
        "y": y,
        "width": width,
        "height": 30,
        "angle": 0,
        "strokeColor": "#868e96",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": generate_seed(),
        "version": 1,
        "versionNonce": generate_seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": 18,
        "fontFamily": 3,
        "textAlign": "center",
        "verticalAlign": "top",
        "containerId": None,
        "originalText": text,
        "lineHeight": 1.25
    }


def convert_to_excalidraw(map: HypothesisMap, title: str = "Карта гипотез") -> str:
    """
    Конвертирует карту гипотез в Excalidraw JSON.

    Раскладка горизонтальная (слева направо):
    Цель → Субъекты → Гипотезы → Задачи
    """
    elements = []
    positions = {}  # {element_id: (x, y, width, height, card_id)}
    card_elements = {}  # {card_id: element_dict} для обновления boundElements

    # Параметры раскладки
    COL_GOAL = 100
    COL_SUBJECT = 500
    COL_HYPOTHESIS = 950
    COL_TASK = 1400

    TITLE_Y = 10
    HEADER_Y = 60
    ROW_START = 110
    ROW_SPACING = 180

    GOAL_W, GOAL_H = 320, 200
    SUBJECT_W, SUBJECT_H = 280, 200
    HYPOTHESIS_W, HYPOTHESIS_H = 380, 350
    TASK_W, TASK_H = 240, 100

    # === НАЗВАНИЕ КАРТЫ ===
    title_elem = {
        "id": f"title-{generate_id()}",
        "type": "text",
        "x": COL_GOAL,
        "y": TITLE_Y,
        "width": COL_TASK + TASK_W - COL_GOAL,
        "height": 36,
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": generate_seed(),
        "version": 1,
        "versionNonce": generate_seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "text": title,
        "fontSize": 28,
        "fontFamily": 3,
        "textAlign": "left",
        "verticalAlign": "top",
        "containerId": None,
        "originalText": title,
        "lineHeight": 1.25
    }
    elements.append(title_elem)

    # === ЗАГОЛОВКИ КОЛОНОК ===
    elements.append(create_label("ЦЕЛЬ", COL_GOAL, HEADER_Y, GOAL_W))
    elements.append(create_label("СУБЪЕКТЫ", COL_SUBJECT, HEADER_Y, SUBJECT_W))
    elements.append(create_label("ГИПОТЕЗЫ", COL_HYPOTHESIS, HEADER_Y, HYPOTHESIS_W))
    elements.append(create_label("ЗАДАЧИ", COL_TASK, HEADER_Y, TASK_W))

    # === ЦЕЛИ ===
    y = ROW_START
    for i, goal in enumerate(map.goals):
        card_id = f"goal-{i}"
        text_id = f"goal-text-{i}"

        text = f"ЦЕЛЬ\n{goal.description}\n"
        if goal.metrics:
            text += "\nМетрики:\n"
            for m in goal.metrics[:3]:
                text += f"• {m.name}: {m.current_value} → {m.target_value}\n"
        if goal.balancing_metrics:
            text += "\nБалансирующие:\n"
            for m in goal.balancing_metrics[:2]:
                text += f"• {m.name}\n"

        rect, txt = create_card(card_id, text_id, COL_GOAL, y, GOAL_W, GOAL_H, COLORS["goal"], text.strip(), 12)
        elements.extend([rect, txt])
        card_elements[card_id] = rect
        positions[goal.id] = (COL_GOAL, y, GOAL_W, GOAL_H, card_id)
        y += GOAL_H + ROW_SPACING

    # === СУБЪЕКТЫ ===
    y = ROW_START
    for i, subject in enumerate(map.subjects):
        card_id = f"subject-{i}"
        text_id = f"subject-text-{i}"

        text = f"СУБЪЕКТ\n{subject.description}\n"
        if subject.pains_desires:
            pains = [p for p in subject.pains_desires if 'боль' in p.lower() or 'страх' in p.lower()]
            desires = [p for p in subject.pains_desires if p not in pains]
            if pains:
                text += "\nБоли:\n" + "\n".join(f"• {p}" for p in pains[:3])
            if desires:
                text += "\n\nЖелания:\n" + "\n".join(f"• {d}" for d in desires[:3])

        rect, txt = create_card(card_id, text_id, COL_SUBJECT, y, SUBJECT_W, SUBJECT_H, COLORS["subject"], text.strip(), 11)
        elements.extend([rect, txt])
        card_elements[card_id] = rect
        positions[subject.id] = (COL_SUBJECT, y, SUBJECT_W, SUBJECT_H, card_id)
        y += SUBJECT_H + ROW_SPACING

    # === ГИПОТЕЗЫ ===
    y = ROW_START
    for i, hyp in enumerate(map.hypotheses):
        card_id = f"hypothesis-{i}"
        text_id = f"hypothesis-text-{i}"

        priority_label = {Priority.HIGH: "🔴 Высокий", Priority.MEDIUM: "🟡 Средний", Priority.LOW: "🟢 Низкий"}.get(hyp.priority, "")

        text = f"ГИПОТЕЗА {i+1}"
        if priority_label:
            text += f"\n{priority_label} приоритет"
        # Переносим каждую часть гипотезы отдельно
        if_wrapped = wrap_text(hyp.if_part, 40)
        then_wrapped = wrap_text(hyp.then_part, 40)
        because_wrapped = wrap_text(hyp.because_part, 40)
        result_wrapped = wrap_text(hyp.then_metric, 40)
        text += f"\n\nЕСЛИ {if_wrapped},\n\nТО {then_wrapped},\n\nПОТОМУ ЧТО {because_wrapped},\n\nТОГДА {result_wrapped}"

        rect, txt = create_card(card_id, text_id, COL_HYPOTHESIS, y, HYPOTHESIS_W, HYPOTHESIS_H, COLORS["hypothesis"], text.strip(), 11)
        elements.extend([rect, txt])
        card_elements[card_id] = rect
        positions[hyp.id] = (COL_HYPOTHESIS, y, HYPOTHESIS_W, HYPOTHESIS_H, card_id)
        y += HYPOTHESIS_H + ROW_SPACING

    # === ЗАДАЧИ ===
    # Группируем задачи по гипотезам
    tasks_by_hypothesis = {}
    for task in map.tasks:
        if task.hypothesis_id not in tasks_by_hypothesis:
            tasks_by_hypothesis[task.hypothesis_id] = []
        tasks_by_hypothesis[task.hypothesis_id].append(task)

    task_idx = 0
    for hyp in map.hypotheses:
        hyp_tasks = tasks_by_hypothesis.get(hyp.id, [])
        if hyp_tasks:
            hyp_pos = positions.get(hyp.id)
            if hyp_pos:
                hyp_y = hyp_pos[1]
                hyp_h = hyp_pos[3]
                # Центрируем задачи относительно гипотезы
                total_tasks_h = len(hyp_tasks) * TASK_H + (len(hyp_tasks) - 1) * 15
                task_start_y = hyp_y + (hyp_h - total_tasks_h) / 2

                for j, task in enumerate(hyp_tasks):
                    card_id = f"task-{task_idx}"
                    text_id = f"task-text-{task_idx}"
                    task_y = task_start_y + j * (TASK_H + 15)

                    wrapped_desc = wrap_text(task.description, max_chars_per_line=25)
                    rect, txt = create_card(card_id, text_id, COL_TASK, task_y, TASK_W, TASK_H, COLORS["task"], wrapped_desc, 12)
                    elements.extend([rect, txt])
                    card_elements[card_id] = rect
                    positions[task.id] = (COL_TASK, task_y, TASK_W, TASK_H, card_id)
                    task_idx += 1

    # === СТРЕЛКИ ===
    arrow_idx = 0
    arrows = []

    def add_arrow_binding(card_id: str, arrow_id: str):
        """Добавляет привязку стрелки к карточке."""
        if card_id in card_elements:
            card_elements[card_id]["boundElements"].append({"id": arrow_id, "type": "arrow"})

    # Субъект → Цель
    for subject in map.subjects:
        if map.goals and subject.id in positions:
            s_pos = positions[subject.id]
            g_pos = positions[map.goals[0].id]
            arrow_id = f"arrow-{arrow_idx}"

            arrow = create_arrow(
                arrow_id,
                s_pos[4], g_pos[4],
                s_pos[0], s_pos[1] + s_pos[3] / 2,
                g_pos[0] + g_pos[2], g_pos[1] + g_pos[3] / 2,
                COLORS["subject"], 3
            )
            arrows.append(arrow)
            add_arrow_binding(s_pos[4], arrow_id)
            add_arrow_binding(g_pos[4], arrow_id)
            arrow_idx += 1

    # Гипотеза → Субъект
    for hyp in map.hypotheses:
        if hyp.subject_id and hyp.subject_id in positions and hyp.id in positions:
            h_pos = positions[hyp.id]
            s_pos = positions[hyp.subject_id]
            arrow_id = f"arrow-{arrow_idx}"

            color = PRIORITY_COLORS.get(hyp.priority, PRIORITY_COLORS[Priority.NONE])
            stroke = PRIORITY_STROKE.get(hyp.priority, 2)

            arrow = create_arrow(
                arrow_id,
                h_pos[4], s_pos[4],
                h_pos[0], h_pos[1] + h_pos[3] / 2,
                s_pos[0] + s_pos[2], s_pos[1] + s_pos[3] / 2,
                color, stroke
            )
            arrows.append(arrow)
            add_arrow_binding(h_pos[4], arrow_id)
            add_arrow_binding(s_pos[4], arrow_id)
            arrow_idx += 1

    # Задача → Гипотеза
    for task in map.tasks:
        if task.hypothesis_id in positions and task.id in positions:
            t_pos = positions[task.id]
            h_pos = positions[task.hypothesis_id]
            arrow_id = f"arrow-{arrow_idx}"

            arrow = create_arrow(
                arrow_id,
                t_pos[4], h_pos[4],
                t_pos[0], t_pos[1] + t_pos[3] / 2,
                h_pos[0] + h_pos[2], h_pos[1] + h_pos[3] / 2,
                "#70736d", 2
            )
            arrows.append(arrow)
            add_arrow_binding(t_pos[4], arrow_id)
            add_arrow_binding(h_pos[4], arrow_id)
            arrow_idx += 1

    # Добавляем стрелки в конец (после обновления boundElements)
    elements.extend(arrows)

    # Формируем итоговый JSON
    excalidraw_data = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": "#ffffff"
        },
        "files": {}
    }

    return json.dumps(excalidraw_data, ensure_ascii=False, indent=2)


def map_from_dict(data: Dict[str, Any]) -> HypothesisMap:
    """Собирает HypothesisMap из вложенного dict (формат map.json, см. SKILL.md)."""
    def metrics(items):
        return [Metric(name=m["name"], current_value=str(m.get("current", "")),
                       target_value=str(m.get("target", ""))) for m in items or []]

    m = HypothesisMap()
    g = data["goal"]
    m.goals.append(Goal(description=g["description"], metrics=metrics(g.get("metrics")),
                        balancing_metrics=metrics(g.get("balancing"))))
    for s in data.get("subjects", []):
        subject = Subject(description=s["name"], pains_desires=list(s.get("pains_desires", [])))
        m.subjects.append(subject)
        for h in s.get("hypotheses", []):
            hyp = Hypothesis(if_part=h["if"], then_part=h["then"], because_part=h["because"],
                             then_metric=h["result"], subject_id=subject.id,
                             priority=Priority(h.get("priority", "none")))
            m.hypotheses.append(hyp)
            m.tasks += [Task(description=t, hypothesis_id=hyp.id) for t in h.get("tasks", [])]
    return m


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        sys.exit("usage: python3 excalidraw_converter.py map.json out.excalidraw")
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(convert_to_excalidraw(map_from_dict(data), title=data.get("title", "Карта гипотез")))
    print(f"✅ Файл создан: {sys.argv[2]}")
