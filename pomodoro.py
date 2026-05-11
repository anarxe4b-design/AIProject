"""
番茄钟桌面应用 - Pomodoro Timer Desktop App
A feature-rich Pomodoro timer built with Python tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import time
import json
import os
import base64
import threading
import platform
from datetime import datetime, timedelta
from pathlib import Path


# === Configuration ===
CONFIG_FILE = Path.home() / ".pomodoro_config.json"
TASKS_FILE = Path.home() / ".pomodoro_tasks.json"
STATS_FILE = Path.home() / ".pomodoro_stats.json"

COLORS = {
    "dark": {
        "bg": "#1a1a2e",
        "bg2": "#16213e",
        "bg3": "#0f3460",
        "accent": "#e94560",
        "accent2": "#533483",
        "text": "#eaeaea",
        "text2": "#a0a0b0",
        "text3": "#666680",
        "success": "#2ecc71",
        "warning": "#f39c12",
        "card": "#1e2746",
        "border": "#2a3250",
        "input_bg": "#252d4a",
        "progress_bg": "#252d4a",
    },
    "light": {
        "bg": "#f5f5f5",
        "bg2": "#ffffff",
        "bg3": "#e8e8e8",
        "accent": "#e74c3c",
        "accent2": "#9b59b6",
        "text": "#2c3e50",
        "text2": "#7f8c8d",
        "text3": "#bdc3c7",
        "success": "#27ae60",
        "warning": "#f1c40f",
        "card": "#ffffff",
        "border": "#e0e0e0",
        "input_bg": "#ffffff",
        "progress_bg": "#ecf0f1",
    }
}

# Default durations (in minutes)
DEFAULT_DURATIONS = {
    "pomodoro": 25,
    "short_break": 5,
    "long_break": 15,
}
LONG_BREAK_INTERVAL = 4  # Long break every N pomodoros

# Embedded favicon (base64 encoded .ico)
FAVICON_B64 = "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//8Ac///AHL+/wBx/f8AcPz/AG/7/wBu+v8Abfn/AGz4/wBr9/8Aavb/AGn1/wA8yP8AAAAAAAAAAAAAAAAAPMj/AIT//wCD//8Agv//AIH//wCA//8Af///AH7//wB9//8AfP//AHv//wB6//8Aef//AHj//wB3//8Adv//AHX//wB0//8Ac///AHL+/wBx/f8AcPz/AG/7/wBu+v8Abfn/AGz4/wBr9/8Aavb/ADzI/wAAAAAAAAAAADzI/wCG//8Ahf//AIT//wCD//8Agv//AIH//wCA//8Af///AH7//wB9//8AfP//AHv//wB6//8Aef//AHj//wB3//8Adv//AHX//wB0//8Ac///AHL+/wBx/f8AcPz/AG/7/wBu+v8Abfn/AGz4/wBr9/8Aavb/ADzI/wAAAAAAAAAAADzI/wCG//8Ahf//AIT//wCD//8Agv//AIH//wCA//8Af///AH7//wB9//8AfP//AHv//wB6//8Aef//AHj//wB3//8Adv//AHX//wB0//8Ac///AHL+/wBx/f8AcPz/AG/7/wBu+v8Abfn/AGz4/wA8yP8AAAAAAAAAAAAAAAAAPMj/AIf//wCG//8Ahf//AIT//wCD//8Agv//AIH//wCA//8Af///AH7//wB9//8AfP//AHv//wB6//8Aef//AHj//wB3//8Adv//AHX//wB0//8Ac///AHL+/wBx/f8AcPz/AG/7/wBu+v8Abfn/ADzI/wAAAAAAAAAAAAAAAAA8yP8AiP//AIf//wCG//8Ahf//AIT//wCD//8Agv//AIH//wCA//8Af///AH7//wB9//8AfP//AHv//wB6//8Aef//AHj//wB3//8Adv//AHX//wB0//8Ac///AHL+/wBx/f8AcPz/AG/7/wBu+v8APMj/AAAAAAAAAAAAAAAAADzI/wCJ//8AiP//AIf//wDIHsgAyB7IAMgeyADIHsgAyB7IAMgeyADIHsgAyB7IAMgeyAB9//8AfP//AHv//wDIHsgAyB7IAMgeyADIHsgAyB7IAMgeyADIHsgAyB7IAMgeyABx/f8AcPz/AG/7/wA8yP8AAAAAAAAAAAAAAAAAPMj/AIr//wCJ//8AiP//AMgeyADIHsgAyB7IAMgeyADIHsgAyB7IAMgeyADIHsgAyB7IAH7//wB9//8AfP//AMgeyADIHsgAyB7IAMgeyADIHsgAyB7IAMgeyADIHsgAyB7IAHL+/wBx/f8AcPz/ADzI/wAAAAAAAAAAAAAAAAAAAAAAPMj/AIr//wCJ//8AyB7IAMgeyADIHsgAyB7IAMgeyADIHsgAyB7IAMgeyADIHsgAf///AH7//wB9//8AyB7IAMgeyADIHsgAyB7IAMgeyADIHsgAyB7IAMgeyADIHsgAc///AHL+/wA8yP8AAAAAAAAAAAAAAAAAAAAAAAAAAAA8yP8Ai///AIr//wDIHsgAyB7IAMgeyADIHsgAyB7IALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AyB7IAMgeyADIHsgAyB7IAMgeyAB0//8Ac///ADzI/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8yP8Ai///AMgeyADIHsgAyB7IAMgeyADIHsgAtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wDIHsgAyB7IAMgeyADIHsgAyB7IAHX//wA8yP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADzI/wA8yP8AyB7IAMgeyADIHsgAyB7IAMgeyAC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/AMgeyADIHsgAyB7IAMgeyADIHsgAPMj/ADzI/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADzI/wDIHsgAyB7IAMgeyADIHsgAyB7IALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AyB7IAMgeyADIHsgAyB7IAMgeyAA8yP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMgeyADIHsgAyB7IAMgeyADIHsgAtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wDIHsgAyB7IAMgeyADIHsgAyB7IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAyB7IAMgeyADIHsgAyB7IAMgeyAC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/AMgeyADIHsgAyB7IAMgeyADIHsgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8yP8APMj/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8AtBT/ALQU/wC0FP8APMj/ADzI/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPMj/ADzI/wA8yP8APMj/ADzI/wCG//8APMj/ADzI/wA8yP8APMj/ADzI/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADzI/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"



# === Timer Engine ===
class TimerEngine:
    """Core timer logic running in a separate thread."""

    def __init__(self):
        self.remaining = 0
        self.total = 0
        self.running = False
        self.paused = False
        self.mode = "pomodoro"  # pomodoro, short_break, long_break
        self._thread = None
        self._lock = threading.Lock()
        self.callbacks = {
            "tick": None,
            "finished": None,
            "mode_change": None,
            "state_change": None,
        }

    def set_mode(self, mode, duration_minutes):
        self.mode = mode
        self.total = duration_minutes * 60
        self.remaining = self.total
        if self.callbacks.get("mode_change"):
            self.callbacks["mode_change"](mode)

    def start(self):
        if self.running:
            return
        self.running = True
        self.paused = False
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        if self.callbacks.get("state_change"):
            self.callbacks["state_change"]("running")

    def pause(self):
        with self._lock:
            self.paused = True
        if self.callbacks.get("state_change"):
            self.callbacks["state_change"]("paused")

    def resume(self):
        with self._lock:
            self.paused = False
        if self.callbacks.get("state_change"):
            self.callbacks["state_change"]("running")

    def stop(self):
        with self._lock:
            self.running = False
            self.paused = False
        if self.callbacks.get("state_change"):
            self.callbacks["state_change"]("stopped")

    def reset(self):
        self.stop()
        self.remaining = self.total
        if self.callbacks.get("tick"):
            self.callbacks["tick"](self.remaining, self.total)

    def _run(self):
        while self.running and self.remaining > 0:
            with self._lock:
                if self.paused:
                    time.sleep(0.1)
                    continue
            time.sleep(0.5)
            with self._lock:
                if not self.running:
                    break
                self.remaining = max(0, self.remaining - 0.5)
            if self.callbacks.get("tick"):
                self.callbacks["tick"](self.remaining, self.total)

        with self._lock:
            if self.running and self.remaining <= 0:
                self.running = False
                if self.callbacks.get("finished"):
                    self.callbacks["finished"](self.mode)


def _json_save(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def _json_load(path, default):
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default


# === Task Manager ===
class TaskManager:
    """Manages the task list."""

    def __init__(self):
        self.tasks = []
        self.load()

    def add(self, text):
        task = {
            "id": str(time.time()),
            "text": text,
            "done": False,
            "created": datetime.now().isoformat(),
        }
        self.tasks.append(task)
        self.save()
        return task

    def toggle(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["done"] = not task["done"]
                self.save()
                return True
        return False

    def delete(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save()

    def clear_done(self):
        self.tasks = [t for t in self.tasks if not t["done"]]
        self.save()

    def save(self):
        _json_save(TASKS_FILE, self.tasks)

    def load(self):
        self.tasks = _json_load(TASKS_FILE, [])


# === Statistics ===
class Statistics:
    """Tracks usage statistics."""

    def __init__(self):
        self.data = {
            "total_pomodoros": 0,
            "total_work_seconds": 0,
            "total_break_seconds": 0,
            "today_pomodoros": 0,
            "current_streak": 0,
            "best_streak": 0,
            "daily_history": {},
            "sessions": [],
        }
        self.load()

    def record_session(self, mode, duration_seconds, completed=True):
        if not completed:
            return
        today = datetime.now().date().isoformat()
        self.data["sessions"].append({
            "date": today,
            "mode": mode,
            "duration": duration_seconds,
            "time": datetime.now().isoformat(),
        })

        if mode == "pomodoro":
            self.data["total_pomodoros"] += 1
            self.data["total_work_seconds"] += duration_seconds
            self.data["daily_history"][today] = self.data["daily_history"].get(today, 0) + 1
            self.data["today_pomodoros"] = self.data["daily_history"].get(today, 0)
            # Streak
            self.data["current_streak"] += 1
            if self.data["current_streak"] > self.data["best_streak"]:
                self.data["best_streak"] = self.data["current_streak"]
        else:
            self.data["total_break_seconds"] += duration_seconds

        self.save()

    def reset_streak(self):
        self.data["current_streak"] = 0
        self.save()

    def save(self):
        _json_save(STATS_FILE, self.data)

    def load(self):
        loaded = _json_load(STATS_FILE, {})
        if loaded:
            self.data.update(loaded)
        today = datetime.now().date().isoformat()
        self.data["today_pomodoros"] = self.data["daily_history"].get(today, 0)


# === Settings ===
class Settings:
    """Persistent user settings."""

    def __init__(self):
        self.data = {
            "theme": "dark",
            "durations": dict(DEFAULT_DURATIONS),
            "auto_start_break": True,
            "auto_start_pomodoro": True,
            "sound_enabled": True,
            "notification_enabled": True,
            "long_break_interval": 4,
            "window_geometry": None,
        }
        self.load()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def save(self):
        _json_save(CONFIG_FILE, self.data)

    def load(self):
        loaded = _json_load(CONFIG_FILE, {})
        if loaded:
            self.data.update(loaded)


# === Main Application ===
class PomodoroApp:
    """Main tkinter application."""

    MODE_COLORS = {
        "pomodoro": "accent",
        "short_break": "success",
        "long_break": "warning",
    }
    MODE_NAMES_CN = {
        "pomodoro": "专注",
        "short_break": "短休",
        "long_break": "长休",
    }
    MODE_STATUS_CN = {
        "pomodoro": "专注时间",
        "short_break": "短暂休息",
        "long_break": "长休息时间",
    }

    def __init__(self):
        self.settings = Settings()
        self.timer = TimerEngine()
        self.tasks = TaskManager()
        self.stats = Statistics()

        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")
        self.root.minsize(420, 600)

        geo = self.settings.get("window_geometry")
        if geo:
            try:
                self.root.geometry(geo)
            except Exception:
                pass
        if not geo:
            self.root.geometry("480x720")

        # Theme
        self.theme = self.settings.get("theme", "dark")
        self.colors = COLORS[self.theme]

        # State
        self.current_mode = "pomodoro"
        self.pomodoro_count = 0
        self._notification_active = False
        self._current_task_var = tk.StringVar()
        self._emoji_font = ("Segoe UI Emoji", 12) if platform.system() == "Windows" else self.font_small
        self._symbol_font = ("Segoe UI", 12) if platform.system() == "Windows" else self.font_tiny

        self._setup_styles()
        self._setup_icon()
        self._build_ui()
        self._bind_shortcuts()

        self.timer.callbacks["tick"] = self._on_tick
        self.timer.callbacks["finished"] = self._on_finished

        self._set_timer_mode("pomodoro")

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._apply_theme()

    # === Icon ===
    def _setup_icon(self):
        ico_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "favicon.ico")
        try:
            if not os.path.exists(ico_path):
                with open(ico_path, "wb") as f:
                    f.write(base64.b64decode(FAVICON_B64))
            self.root.iconbitmap(ico_path)
        except Exception:
            pass

    # === UI Setup ===
    def _setup_styles(self):
        self.root.configure(bg=self.colors["bg"])

        font_defs = [
            ("font_large", 56, "bold"),
            ("font_medium", 14, "normal"),
            ("font_small", 11, "normal"),
            ("font_tiny", 9, "normal"),
            ("font_task", 12, "normal"),
            ("font_timer_small", 24, "bold"),
            ("font_title", 16, "bold"),
        ]
        for name, size, weight in font_defs:
            try:
                setattr(self, name, font.Font(family="Helvetica", size=size, weight=weight))
            except Exception:
                setattr(self, name, font.Font(size=size, weight=weight))

    def _build_ui(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # === Header ===
        self._build_header()

        # === Mode Selector ===
        self._build_mode_selector()

        # === Timer Display ===
        self._build_timer_display()

        # === Controls ===
        self._build_controls()

        # === Progress Bar ===
        self._build_progress()

        # === Stats ===
        self._build_stats()

        # === Separator ===
        sep = tk.Frame(self.main_frame, height=1, bg=self.colors["border"])
        sep.pack(fill=tk.X, padx=30, pady=(0, 10))

        # === Task Section ===
        self._build_task_section()

        # Footer spacer
        tk.Frame(self.main_frame, height=10, bg=self.colors["bg"]).pack()

    def _build_header(self):
        header = tk.Frame(self.main_frame, bg=self.colors["bg"])
        header.pack(fill=tk.X, padx=20, pady=(15, 5))

        tk.Label(
            header,
            text="POMODORO",
            font=self.font_title,
            bg=self.colors["bg"],
            fg=self.colors["accent"],
        ).pack(side=tk.LEFT)

        self.help_btn = tk.Label(
            header,
            text="?",
            font=self.font_medium,
            bg=self.colors["bg"],
            fg=self.colors["text2"],
            cursor="hand2",
        )
        self.help_btn.pack(side=tk.RIGHT, padx=5)
        self.help_btn.bind("<Button-1>", lambda e: self._show_help())

        self.stats_btn = tk.Label(
            header,
            text="📊",
            font=self.font_medium,
            bg=self.colors["bg"],
            fg=self.colors["text2"],
            cursor="hand2",
        )
        self.stats_btn.pack(side=tk.RIGHT, padx=2)
        self.stats_btn.bind("<Button-1>", lambda e: self._show_stats_dialog())

        self.theme_btn = tk.Label(
            header,
            text="☀" if self.theme == "dark" else "☾",
            font=self.font_medium,
            bg=self.colors["bg"],
            fg=self.colors["text2"],
            cursor="hand2",
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=5)
        self.theme_btn.bind("<Button-1>", lambda e: self._toggle_theme())

        self.settings_btn = tk.Label(
            header,
            text="⚙",
            font=self.font_medium,
            bg=self.colors["bg"],
            fg=self.colors["text2"],
            cursor="hand2",
        )
        self.settings_btn.pack(side=tk.RIGHT, padx=2)
        self.settings_btn.bind("<Button-1>", lambda e: self._show_settings())

    def _build_mode_selector(self):
        self.mode_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.mode_frame.pack(fill=tk.X, padx=30, pady=(5, 5))

        self.mode_btns = {}
        modes = [
            ("pomodoro", "🍅 专注"),
            ("short_break", "☕ 短休"),
            ("long_break", "🌙 长休"),
        ]

        for i, (mode_key, label) in enumerate(modes):
            btn = tk.Label(
                self.mode_frame,
                text=label,
                font=self.font_small,
                bg=self.colors["bg"],
                fg=self.colors["text2"],
                cursor="hand2",
                padx=12,
                pady=6,
            )
            btn.pack(side=tk.LEFT, padx=(0 if i == 0 else 5, 0))
            btn.bind("<Button-1>", lambda e, m=mode_key: self._set_timer_mode(m))
            self.mode_btns[mode_key] = btn

    def _build_timer_display(self):
        timer_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        timer_frame.pack(fill=tk.X, padx=30, pady=(10, 5))

        self.round_label = tk.Label(
            timer_frame,
            text="",
            font=self.font_tiny,
            bg=self.colors["bg"],
            fg=self.colors["text3"],
        )
        self.round_label.pack()

        self.timer_label = tk.Label(
            timer_frame,
            text="25:00",
            font=self.font_large,
            bg=self.colors["bg"],
            fg=self.colors["accent"],
        )
        self.timer_label.pack(pady=(0, 0))

        # Status text
        self.status_label = tk.Label(
            timer_frame,
            text="点击开始专注",
            font=self.font_small,
            bg=self.colors["bg"],
            fg=self.colors["text2"],
        )
        self.status_label.pack(pady=(0, 5))

    def _build_controls(self):
        control_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        control_frame.pack(fill=tk.X, padx=30, pady=(5, 10))

        btn_container = tk.Frame(control_frame, bg=self.colors["bg"])
        btn_container.pack()

        self.start_btn = self._create_button(
            btn_container,
            "▶  开始",
            self._toggle_timer,
            self.colors["accent"],
            self.colors["bg"],
        )
        self.start_btn.pack(side=tk.LEFT, padx=3)

        self.reset_btn = self._create_button(
            btn_container,
            "↻  重置",
            self._reset_timer,
            self.colors["card"],
            self.colors["text"],
        )
        self.reset_btn.pack(side=tk.LEFT, padx=3)

    def _create_button(self, parent, text, callback, bg=None, fg=None):
        if bg is None:
            bg = self.colors["card"]
        if fg is None:
            fg = self.colors["text"]

        btn = tk.Label(
            parent,
            text=text,
            font=self.font_small,
            bg=bg,
            fg=fg,
            cursor="hand2",
            padx=18,
            pady=8,
        )
        btn.bind("<Button-1>", lambda e: callback())
        return btn

    def _build_progress(self):
        self.progress_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.progress_frame.pack(fill=tk.X, padx=30, pady=(0, 10))

        self.progress_canvas = tk.Canvas(
            self.progress_frame,
            height=6,
            bg=self.colors["progress_bg"],
            highlightthickness=0,
        )
        self.progress_canvas.pack(fill=tk.X)
        self.progress_bar = self.progress_canvas.create_rectangle(
            0, 0, 0, 6,
            fill=self.colors["accent"],
            width=0,
        )

    def _build_stats(self):
        stats_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        stats_frame.pack(fill=tk.X, padx=30, pady=(0, 5))

        # Today's count
        self.stats_label = tk.Label(
            stats_frame,
            text="",
            font=self.font_tiny,
            bg=self.colors["bg"],
            fg=self.colors["text3"],
        )
        self.stats_label.pack()

        self._update_stats_display()

    def _build_task_section(self):
        task_section = tk.Frame(self.main_frame, bg=self.colors["bg"])
        task_section.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        # Task header
        task_header = tk.Frame(task_section, bg=self.colors["bg"])
        task_header.pack(fill=tk.X)
        tk.Label(
            task_header,
            text="📋 任务列表",
            font=self.font_small,
            bg=self.colors["bg"],
            fg=self.colors["text2"],
        ).pack(side=tk.LEFT)

        clear_btn = tk.Label(
            task_header,
            text="清除已完成",
            font=self.font_tiny,
            bg=self.colors["bg"],
            fg=self.colors["text3"],
            cursor="hand2",
        )
        clear_btn.pack(side=tk.RIGHT)
        clear_btn.bind("<Button-1>", lambda e: self._clear_done_tasks())

        # Task input
        input_frame = tk.Frame(task_section, bg=self.colors["bg"])
        input_frame.pack(fill=tk.X, pady=(5, 5))

        self.task_entry = tk.Entry(
            input_frame,
            font=self.font_task,
            bg=self.colors["input_bg"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief=tk.FLAT,
            bd=8,
            highlightthickness=1,
            highlightcolor=self.colors["border"],
            highlightbackground=self.colors["border"],
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.task_entry.bind("<Return>", lambda e: self._add_task())

        add_btn = tk.Label(
            input_frame,
            text="＋",
            font=self.font_medium,
            bg=self.colors["accent"],
            fg="white",
            cursor="hand2",
            padx=12,
            pady=4,
        )
        add_btn.pack(side=tk.RIGHT, padx=(5, 0))
        add_btn.bind("<Button-1>", lambda e: self._add_task())

        # Task list
        task_list_frame = tk.Frame(task_section, bg=self.colors["bg"])
        task_list_frame.pack(fill=tk.BOTH, expand=True)

        self.task_canvas = tk.Canvas(
            task_list_frame,
            bg=self.colors["bg"],
            highlightthickness=0,
        )
        self.task_scrollbar = tk.Scrollbar(
            task_list_frame,
            orient=tk.VERTICAL,
            command=self.task_canvas.yview,
        )
        self.task_scrollable_frame = tk.Frame(self.task_canvas, bg=self.colors["bg"])

        self.task_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.task_canvas.configure(
                scrollregion=self.task_canvas.bbox("all")
            ),
        )
        self._task_canvas_window = self.task_canvas.create_window(
            (0, 0),
            window=self.task_scrollable_frame,
            anchor="nw",
            width=self.task_canvas.winfo_width(),
        )
        self.task_canvas.configure(yscrollcommand=self.task_scrollbar.set)

        self.task_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind resize
        self.task_canvas.bind("<Configure>", self._on_task_canvas_resize)

        # Render tasks
        self._render_tasks()

    def _on_task_canvas_resize(self, event):
        self.task_canvas.itemconfig(self._task_canvas_window, width=event.width)

    def _bind_shortcuts(self):
        self.root.bind("<space>", lambda e: self._toggle_timer())
        self.root.bind("<r>", lambda e: self._reset_timer())
        self.root.bind("<Escape>", lambda e: self._reset_timer())

    # === Theme ===
    def _apply_theme(self):
        self.colors = COLORS[self.theme]
        bg = self.colors["bg"]

        self.root.configure(bg=bg)
        self.main_frame.configure(bg=bg)

        # Header
        self.theme_btn.configure(bg=bg, fg=self.colors["text2"])
        self.theme_btn.configure(text="☀" if self.theme == "dark" else "☾")
        self.settings_btn.configure(bg=bg, fg=self.colors["text2"])
        self.help_btn.configure(bg=bg, fg=self.colors["text2"])
        self.stats_btn.configure(bg=bg, fg=self.colors["text2"])

        # Mode selector
        self.mode_frame.configure(bg=bg)
        for key, btn in self.mode_btns.items():
            btn.configure(bg=bg)
            if key == self.current_mode:
                btn.configure(fg=self.colors["accent"])
            else:
                btn.configure(fg=self.colors["text2"])

        # Timer
        timer_color = self.colors[self.MODE_COLORS.get(self.current_mode, "accent")]

        for widget in [self.timer_label, self.round_label, self.status_label]:
            widget.configure(bg=bg)
        if self.round_label:
            self.round_label.configure(fg=self.colors["text3"])
        if self.status_label:
            self.status_label.configure(fg=self.colors["text2"])
        if self.timer_label:
            self.timer_label.configure(fg=timer_color)

        # Controls
        for btn in [self.start_btn, self.reset_btn]:
            btn.configure(bg=bg)

        # Progress
        self.progress_frame.configure(bg=bg)
        self.progress_canvas.configure(bg=self.colors["progress_bg"])
        self._update_progress()

        # Stats
        self.stats_label.configure(bg=bg, fg=self.colors["text3"])

        # Task section

        self._render_tasks()

    def _toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.settings.set("theme", self.theme)
        self.colors = COLORS[self.theme]
        self._apply_theme()

    # === Mode Management ===
    def _set_timer_mode(self, mode):
        # Don't switch if timer is running
        if self.timer.running:
            return

        self.current_mode = mode
        durations = self.settings.get("durations", DEFAULT_DURATIONS)
        duration_map = {
            "pomodoro": durations["pomodoro"],
            "short_break": durations["short_break"],
            "long_break": durations["long_break"],
        }

        self.timer.set_mode(mode, duration_map.get(mode, 25))
        self._update_display()

        # Update UI
        for key, btn in self.mode_btns.items():
            btn.configure(
                fg=self.colors["accent"] if key == mode else self.colors["text2"]
            )

        # Update timer color
        timer_color = self.colors[self.MODE_COLORS.get(mode, "accent")]
        self.timer_label.configure(fg=timer_color)

        # Update status
        self.status_label.configure(text=self.MODE_STATUS_CN.get(mode, ""))

        # Reset start button
        self.start_btn.configure(text="▶  开始", bg=self.colors["accent"])

        # Update round counter
        if mode == "pomodoro":
            self.round_label.configure(
                text=f"第 {self.pomodoro_count + 1} 个番茄"
            )
        else:
            self.round_label.configure(text="")

    # === Timer Controls ===
    def _set_controls(self, text, bg, status):
        self.start_btn.configure(text=text, bg=bg)
        self.status_label.configure(text=status)

    def _toggle_timer(self):
        if self.timer.running:
            if self.timer.paused:
                self.timer.resume()
                self._set_controls("⏸  暂停", self.colors["warning"], "进行中...")
            else:
                self.timer.pause()
                self._set_controls("▶  继续", self.colors["success"], "已暂停")
        else:
            if self.timer.remaining <= 0:
                self._set_timer_mode(self.current_mode)
            self.timer.start()
            self._set_controls("⏸  暂停", self.colors["warning"], "进行中...")

    def _reset_timer(self):
        self.timer.stop()
        self._set_timer_mode(self.current_mode)

    def _auto_start_timer(self):
        self.timer.start()
        self._set_controls("⏸  暂停", self.colors["warning"], "进行中...")

    def _on_tick(self, remaining, total):
        self.root.after(0, self._update_display)

    def _update_display(self):
        remaining = int(self.timer.remaining)
        total = int(self.timer.total)
        mins, secs = divmod(remaining, 60)
        self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")

        self._update_progress()

        mn = self.MODE_NAMES_CN.get(self.current_mode, "番茄钟")
        self.root.title(f"{mins:02d}:{secs:02d} - {mn} - Pomodoro Timer")

    def _update_progress(self):
        total = max(1, self.timer.total)
        progress = 1 - (self.timer.remaining / total)
        width = self.progress_canvas.winfo_width()
        bar_width = int(width * progress)
        self.progress_canvas.coords(self.progress_bar, 0, 0, bar_width, 6)

    def _on_finished(self, mode):
        self.root.after(0, self._handle_finished, mode)

    def _handle_finished(self, mode):
        self.start_btn.configure(text="▶  开始", bg=self.colors["accent"])

        if mode == "pomodoro":
            self.pomodoro_count += 1
            self.stats.record_session("pomodoro", self.timer.total)

            # Show notification
            self._show_notification("番茄完成！", "太棒了！休息一下吧 🎉")

            # Auto-start break
            if self.settings.get("auto_start_break", True):
                interval = self.settings.get("long_break_interval", 4)
                next_mode = "long_break" if self.pomodoro_count % interval == 0 else "short_break"
                self._set_timer_mode(next_mode)
                self._auto_start_timer()
            else:
                self._set_timer_mode("pomodoro")

            self.round_label.configure(text=f"已完成 {self.pomodoro_count} 个番茄")

        else:
            self.stats.record_session(mode, self.timer.total)
            self._show_notification(
                f"{self.MODE_NAMES_CN.get(mode, '休息')}结束！",
                "该继续工作了 💪"
            )

            if self.settings.get("auto_start_pomodoro", False):
                self._set_timer_mode("pomodoro")
                self._auto_start_timer()
            else:
                self._set_timer_mode("pomodoro")

        self._update_stats_display()
        self._play_sound()

    # === Notifications & Sound ===
    def _show_notification(self, title, message):
        if not self.settings.get("notification_enabled", True):
            return

        try:
            if platform.system() == "Windows":
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(
                    title,
                    message,
                    duration=5,
                    threaded=True,
                )
            elif platform.system() == "Darwin":
                os.system(
                    f'osascript -e \'display notification "{message}" '
                    f'with title "{title}"\''
                )
            else:
                os.system(f'notify-send "{title}" "{message}"')
        except Exception:
            # Fallback: use a top-level window
            self._show_popup_notification(title, message)

    def _show_popup_notification(self, title, message):
        if self._notification_active:
            return
        self._notification_active = True

        win = tk.Toplevel(self.root)
        win.title("")
        win.geometry("300x150+{}+{}".format(
            self.root.winfo_x() + 90,
            self.root.winfo_y() + 100,
        ))
        win.configure(bg=self.colors["bg"])
        win.overrideredirect(True)
        win.attributes("-topmost", True)

        # Frame
        frame = tk.Frame(win, bg=self.colors["card"],
                         highlightbackground=self.colors["accent"],
                         highlightthickness=2)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(
            frame,
            text=title,
            font=self.font_medium,
            bg=self.colors["card"],
            fg=self.colors["accent"],
        ).pack(pady=(20, 5))

        tk.Label(
            frame,
            text=message,
            font=self.font_small,
            bg=self.colors["card"],
            fg=self.colors["text"],
        ).pack(pady=5)

        tk.Button(
            frame,
            text="确定",
            command=lambda: self._close_notification(win),
            bg=self.colors["accent"],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
        ).pack(pady=10)

        # Auto-close after 5 seconds
        self.root.after(5000, lambda: self._close_notification(win))

    def _close_notification(self, win):
        try:
            win.destroy()
        except Exception:
            pass
        self._notification_active = False

    def _play_sound(self):
        if not self.settings.get("sound_enabled", True):
            return
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.PlaySound(
                    "SystemExclamation",
                    winsound.SND_ALIAS | winsound.SND_ASYNC,
                )
            else:
                print("\a")
        except Exception:
            pass

    # === Task Management ===
    def _add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return
        self.tasks.add(text)
        self.task_entry.delete(0, tk.END)
        self._render_tasks()

    def _clear_done_tasks(self):
        self.tasks.clear_done()
        self._render_tasks()

    def _render_tasks(self):
        for widget in self.task_scrollable_frame.winfo_children():
            widget.destroy()

        if not self.tasks.tasks:
            empty_label = tk.Label(
                self.task_scrollable_frame,
                text="暂无任务，在上方添加",
                font=self.font_tiny,
                bg=self.colors["bg"],
                fg=self.colors["text3"],
            )
            empty_label.pack(pady=20)
            return

        for task in self.tasks.tasks:
            self._render_task_item(task)

    def _render_task_item(self, task):
        item_frame = tk.Frame(
            self.task_scrollable_frame,
            bg=self.colors["card"],
        )
        item_frame.pack(fill=tk.X, pady=2)

        # Checkbox / status
        status_text = "✅" if task["done"] else "⬜"
        status_btn = tk.Label(
            item_frame,
            text=status_text,
            bg=self.colors["card"],
            fg=self.colors["text2"],
            cursor="hand2",
            font=self._emoji_font,
        )
        status_btn.pack(side=tk.LEFT, padx=(8, 3), pady=5)
        status_btn.bind("<Button-1>", lambda e, tid=task["id"]: self._toggle_task(tid))

        # Task text
        text_color = self.colors["text3"] if task["done"] else self.colors["text"]
        if task["done"]:
            done_font = font.Font(**self.font_task.actual())
            done_font.configure(overstrike=True)

        task_label = tk.Label(
            item_frame,
            text=task["text"],
            font=done_font if task["done"] else self.font_task,
            bg=self.colors["card"],
            fg=text_color,
            anchor=tk.W,
            wraplength=280,
            justify=tk.LEFT,
        )
        task_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5)
        task_label.bind(
            "<Button-1>",
            lambda e, tid=task["id"]: self._toggle_task(tid),
        )

        # Delete button
        del_btn = tk.Label(
            item_frame,
            text="✕",
            bg=self.colors["card"],
            fg=self.colors["text3"],
            cursor="hand2",
            font=self._symbol_font,
        )
        del_btn.pack(side=tk.RIGHT, padx=(0, 8), pady=5)
        del_btn.bind("<Button-1>", lambda e, tid=task["id"]: self._delete_task(tid))

    def _toggle_task(self, task_id):
        self.tasks.toggle(task_id)
        self._render_tasks()

    def _delete_task(self, task_id):
        self.tasks.delete(task_id)
        self._render_tasks()

    # === Statistics Display ===
    def _update_stats_display(self):
        s = self.stats.data
        streak = s.get("current_streak", 0)
        total = s.get("total_pomodoros", 0)
        today = s.get("today_pomodoros", 0)
        self.stats_label.configure(
            text=f"今日: {today} 个  |  总计: {total} 个  |  连续: {streak} 个"
        )

    # === Help Dialog ===
    def _show_help(self):
        win = tk.Toplevel(self.root)
        win.title("使用说明")
        win.geometry("420x500")
        win.configure(bg=self.colors["bg"])
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        self._center_child(win, 420, 500)

        # Title
        tk.Label(
            win, text="🍅 番茄钟使用说明",
            font=self.font_medium,
            bg=self.colors["bg"],
            fg=self.colors["accent"],
        ).pack(pady=(15, 5))

        # Content frame with scroll
        canvas = tk.Canvas(win, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(win, orient=tk.VERTICAL, command=canvas.yview)
        frame = tk.Frame(canvas, bg=self.colors["bg"])

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw", width=380)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))

        sections = [
            ("⏱ 什么是番茄钟？",
             "番茄工作法是一种时间管理方法，"
             "通过 25 分钟专注工作 + 5 分钟休息的循环，"
             "帮助提高效率。每完成 4 个番茄后有一 "
             "次 15 分钟的长休息。"),

            ("▶ 基本操作",
             "• 点击「专注」「短休」「长休」切换模式\n"
             "• 点击「开始」按钮启动计时\n"
             "• 再次点击可暂停，继续点击恢复\n"
             "• 点击「重置」回到当前模式初始时间"),

            ("⌨ 快捷键",
             "• Space — 开始 / 暂停\n"
             "• R — 重置计时器\n"
             "• Esc — 重置计时器\n"
             "• Enter — 添加任务"),

            ("📋 任务管理",
             "• 在输入框中输入任务，按 Enter 或点「＋」添加\n"
             "• 点击任务或方块标记完成 / 取消完成\n"
             "• 点击「✕」删除单个任务\n"
             "• 点击「清除已完成」清理所有已完成任务"),

            ("⚙ 自定义设置",
             "点击右上角 ⚙ 进入设置，可调整：\n"
             "• 专注 / 短休 / 长休 的时长\n"
             "• 是否自动开始休息 / 专注\n"
             "• 是否启用声音和桌面通知"),

            ("🎨 主题切换",
             "点击右上角 ☀/☾ 按钮可在深色和浅色主题之间切换。"),

            ("📊 统计数据",
             "点击右上角 📊 查看已完成番茄数和专注时间统计。"),

            ("💡 小贴士",
             "• 每完成一个番茄，休息一下效果更好\n"
             "• 建议一次只专注一个任务\n"
             "• 番茄钟开始后不会自动切换模式\n"
             "  （可在设置中开启自动切换）\n"
             "• 数据保存在本地，不会上传"),
        ]

        for title, content in sections:
            section_frame = tk.Frame(frame, bg=self.colors["bg"])
            section_frame.pack(fill=tk.X, pady=(10, 5))

            tk.Label(
                section_frame,
                text=title,
                font=self.font_small,
                bg=self.colors["bg"],
                fg=self.colors["accent"],
                anchor=tk.W,
            ).pack(fill=tk.X)

            tk.Label(
                section_frame,
                text=content,
                font=self.font_tiny,
                bg=self.colors["bg"],
                fg=self.colors["text"],
                anchor=tk.W,
                justify=tk.LEFT,
                wraplength=360,
            ).pack(fill=tk.X, pady=(3, 0))

        # Close button
        tk.Button(
            win,
            text="知道了",
            command=win.destroy,
            bg=self.colors["accent"],
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=4,
            cursor="hand2",
            font=self.font_small,
        ).pack(pady=(15, 15))

    # === Settings Dialog ===
    def _show_settings(self):
        win = tk.Toplevel(self.root)
        win.title("设置")
        win.geometry("380x350")
        win.configure(bg=self.colors["bg"])
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        self._center_child(win, 380, 350)

        # Title
        tk.Label(
            win, text="⚙ 设置",
            font=self.font_medium,
            bg=self.colors["bg"],
            fg=self.colors["text"],
        ).pack(pady=(15, 10))

        # Durations
        durations = self.settings.get("durations", DEFAULT_DURATIONS)
        settings_frame = tk.Frame(win, bg=self.colors["bg"])
        settings_frame.pack(padx=30, fill=tk.X)

        duration_vars = {}
        labels = [
            ("pomodoro", "专注时长 (分钟):"),
            ("short_break", "短休时长 (分钟):"),
            ("long_break", "长休时长 (分钟):"),
        ]

        for i, (key, label) in enumerate(labels):
            row = tk.Frame(settings_frame, bg=self.colors["bg"])
            row.pack(fill=tk.X, pady=4)

            tk.Label(
                row, text=label,
                font=self.font_tiny,
                bg=self.colors["bg"],
                fg=self.colors["text2"],
            ).pack(side=tk.LEFT)

            var = tk.StringVar(value=str(durations.get(key, 25)))
            duration_vars[key] = var
            entry = tk.Entry(
                row,
                textvariable=var,
                width=5,
                font=self.font_small,
                bg=self.colors["input_bg"],
                fg=self.colors["text"],
                insertbackground=self.colors["text"],
                relief=tk.FLAT,
                bd=4,
                justify=tk.CENTER,
            )
            entry.pack(side=tk.RIGHT)

        # Options
        options_frame = tk.Frame(win, bg=self.colors["bg"])
        options_frame.pack(padx=30, pady=10, fill=tk.X)

        auto_break_var = tk.BooleanVar(
            value=self.settings.get("auto_start_break", True)
        )
        auto_pomo_var = tk.BooleanVar(
            value=self.settings.get("auto_start_pomodoro", False)
        )
        sound_var = tk.BooleanVar(
            value=self.settings.get("sound_enabled", True)
        )
        notif_var = tk.BooleanVar(
            value=self.settings.get("notification_enabled", True)
        )

        options = [
            ("自动开始休息", auto_break_var),
            ("自动开始专注", auto_pomo_var),
            ("启用声音", sound_var),
            ("启用通知", notif_var),
        ]

        for label, var in options:
            row = tk.Frame(options_frame, bg=self.colors["bg"])
            row.pack(fill=tk.X, pady=2)

            cb = tk.Checkbutton(
                row,
                text=label,
                variable=var,
                bg=self.colors["bg"],
                fg=self.colors["text"],
                selectcolor=self.colors["card"],
                activebackground=self.colors["bg"],
                activeforeground=self.colors["text"],
                font=self.font_tiny,
            )
            cb.pack(side=tk.LEFT)

        # Save button
        def save_settings():
            for key, var in duration_vars.items():
                try:
                    val = int(var.get())
                    if val <= 0:
                        raise ValueError
                    durations[key] = val
                except ValueError:
                    messagebox.showerror("错误", f"{key} 必须为正整数")
                    return

            self.settings.set("durations", durations)
            self.settings.set("auto_start_break", auto_break_var.get())
            self.settings.set("auto_start_pomodoro", auto_pomo_var.get())
            self.settings.set("sound_enabled", sound_var.get())
            self.settings.set("notification_enabled", notif_var.get())

            # Reset current timer if not running
            if not self.timer.running:
                self._set_timer_mode(self.current_mode)

            win.destroy()

        btn_frame = tk.Frame(win, bg=self.colors["bg"])
        btn_frame.pack(pady=(10, 15))

        tk.Button(
            btn_frame,
            text="保存",
            command=save_settings,
            bg=self.colors["accent"],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=4,
            cursor="hand2",
            font=self.font_small,
        ).pack()

    # === Stats Dialog ===
    def _show_stats_dialog(self):
        win = tk.Toplevel(self.root)
        win.title("统计")
        win.geometry("350x300")
        win.configure(bg=self.colors["bg"])
        win.transient(self.root)
        win.grab_set()

        s = self.stats.data
        stats_text = (
            f"总计完成番茄: {s.get('total_pomodoros', 0)} 个\n"
            f"今日完成: {s.get('today_pomodoros', 0)} 个\n"
            f"当前连续: {s.get('current_streak', 0)} 个\n"
            f"最佳连续: {s.get('best_streak', 0)} 个\n"
            f"总专注时间: {s.get('total_work_seconds', 0) // 60} 分钟\n"
            f"总休息时间: {s.get('total_break_seconds', 0) // 60} 分钟\n"
        )

        tk.Label(
            win, text="📊 统计",
            font=self.font_medium,
            bg=self.colors["bg"],
            fg=self.colors["text"],
        ).pack(pady=(15, 10))

        tk.Label(
            win,
            text=stats_text,
            font=self.font_small,
            bg=self.colors["bg"],
            fg=self.colors["text"],
            justify=tk.LEFT,
        ).pack(padx=30, pady=10, anchor=tk.W)

        def reset_stats():
            if messagebox.askyesno("确认", "确定要重置所有统计数据吗？"):
                self.stats.data = {
                    "total_pomodoros": 0,
                    "total_work_seconds": 0,
                    "total_break_seconds": 0,
                    "today_pomodoros": 0,
                    "current_streak": 0,
                    "best_streak": 0,
                    "daily_history": {},
                    "sessions": [],
                }
                self.stats.save()
                self._update_stats_display()
                win.destroy()

        tk.Button(
            win,
            text="重置统计",
            command=reset_stats,
            bg=self.colors["card"],
            fg=self.colors["text3"],
            relief=tk.FLAT,
            padx=15,
            cursor="hand2",
            font=self.font_tiny,
        ).pack(pady=10)

    # === Window Events ===
    def _on_close(self):
        try:
            geo = self.root.geometry()
            self.settings.set("window_geometry", geo)
        except Exception:
            pass

        if self.timer.running:
            if messagebox.askokcancel("退出", "计时器正在运行，确定要退出吗？"):
                self.timer.stop()
                self.root.destroy()
        else:
            self.root.destroy()

    def _center_child(self, win, w, h):
        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - w) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - h) // 2
        win.geometry(f"+{x}+{y}")

    def run(self):
        self.root.mainloop()


# === Entry Point ===
def main():
    app = PomodoroApp()
    app.run()


if __name__ == "__main__":
    main()
