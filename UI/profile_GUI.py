import wx
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from datetime import datetime, timedelta
import numpy as np


class ProfileApp(wx.Frame):
    def __init__(self, *args, user=None, **kwargs):
        super(ProfileApp, self).__init__(*args, **kwargs)

        # Color scheme - matching fitness app
        self.primary_bg = "#EAF2FF"  # Light Blue
        self.card_bg = "#FFFFFF"  # White
        self.header_bg = "#2E5BFF"  # Blue Header
        self.helen_color = "#4A90E2"  # Blue Buttons
        self.helen_hover = "#357ABD"  # Dark Blue Hover
        self.accent_green = "#28A745"  # Green Buttons
        self.green_hover = "#1E7E34"  # Dark Green Hover
        self.text_dark = "#000000"  # Black Text
        self.text_muted = "#333333"  # Dark Gray for Muted Text
        self.border = "#CCCCCC"  # Light Gray for Borders

        # Button text colors
        self.button_text_color = "#000000"

        # User Dataset
        self.current_user = user
        self.conn = None
        self.cursor = None

        # Initialize range_choice with default value
        self.range_choice = None

        self.init_database()
        self.InitUI()

    def init_database(self):
        """Initialize database connection and create profile tables if not exist"""
        try:
            self.conn = sqlite3.connect('./Database/fitness_app.db')
            self.cursor = self.conn.cursor()

            # User Profile Table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    age INTEGER,
                    height REAL,
                    weight REAL,
                    gender TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Weight History Table for tracking progress
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS weight_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    weight REAL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Workout History Table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    workout_type TEXT,
                    duration INTEGER,
                    calories_burned INTEGER,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Diet History Table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS diet_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    meal_type TEXT,
                    calories INTEGER,
                    protein INTEGER,
                    carbs INTEGER,
                    fats INTEGER,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            self.conn.commit()
        except sqlite3.Error as e:
            wx.MessageBox(f"Error initializing database: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def InitUI(self):
        self.SetTitle(f"Smart Fitness Assistant - Profile")
        self.SetSize((1280, 850))
        self.SetMinSize((1100, 700))
        self.SetBackgroundColour(self.primary_bg)

        # Main panel
        panel = wx.Panel(self)
        panel.SetBackgroundColour(self.primary_bg)

        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # HEADER
        header_panel = wx.Panel(panel)
        header_panel.SetBackgroundColour(self.header_bg)
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Title and user info
        title_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(header_panel, label="My Profile and Progress")
        title.SetFont(wx.Font(22, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour("WHITE"))

        if self.current_user:
            user_info = wx.StaticText(
                header_panel,
                label=f"Welcome back, {self.current_user.get('first_name') or self.current_user.get('username')}!"
            )
        else:
            user_info = wx.StaticText(header_panel, label="Welcome to your profile!")

        user_info.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        user_info.SetForegroundColour(wx.Colour("WHITE"))

        title_sizer.Add(title, 0, wx.ALL, 12)
        title_sizer.Add(user_info, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

        # Navigation buttons on header
        nav_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.home_btn = wx.Button(header_panel, label="🏠 Home")
        self.home_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        self.home_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        self.home_btn.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.home_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.home_btn.Bind(wx.EVT_BUTTON, self.on_home)
        self.home_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.home_btn, self.helen_hover)
        )
        self.home_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.home_btn, self.helen_color)
        )

        self.logout_btn = wx.Button(header_panel, label="🚪 Logout")
        self.logout_btn.SetBackgroundColour(wx.Colour("#DC3545"))
        self.logout_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        self.logout_btn.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.logout_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.logout_btn.Bind(wx.EVT_BUTTON, self.on_logout)
        self.logout_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.logout_btn, "#B02A37")
        )
        self.logout_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.logout_btn, "#DC3545")
        )

        nav_sizer.Add(self.home_btn, 0, wx.RIGHT, 10)
        nav_sizer.Add(self.logout_btn, 0)

        header_sizer.Add(title_sizer, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        header_sizer.Add(nav_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)

        header_panel.SetSizer(header_sizer)
        main_sizer.Add(header_panel, 0, wx.EXPAND | wx.ALL, 10)

        # CONTENT AREA
        content_panel = wx.Panel(panel)
        content_panel.SetBackgroundColour(self.primary_bg)
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # LEFT SIDEBAR - User Info & Stats
        left_sidebar = wx.Panel(content_panel)
        left_sidebar.SetBackgroundColour(self.card_bg)
        left_sidebar.SetMinSize((380, -1))
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Profile Picture/Avatar
        avatar_panel = wx.Panel(left_sidebar)
        avatar_panel.SetBackgroundColour(self.primary_bg)
        avatar_sizer = wx.BoxSizer(wx.VERTICAL)

        self.avatar_text = wx.StaticText(avatar_panel, label="🎯")
        self.avatar_text.SetFont(
            wx.Font(80, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.avatar_text.SetForegroundColour(wx.Colour(self.header_bg))

        username_display = wx.StaticText(
            avatar_panel,
            label=self.current_user.get('username') if self.current_user else "Guest User"
        )
        username_display.SetFont(
            wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        username_display.SetForegroundColour(wx.Colour(self.text_dark))

        avatar_sizer.Add(self.avatar_text, 0, wx.ALL | wx.ALIGN_CENTER, 15)
        avatar_sizer.Add(username_display, 0, wx.BOTTOM | wx.ALIGN_CENTER, 15)

        avatar_panel.SetSizer(avatar_sizer)
        left_sizer.Add(avatar_panel, 0, wx.EXPAND | wx.ALL, 15)

        # Quick Stats Card
        stats_card = wx.Panel(left_sidebar)
        stats_card.SetBackgroundColour(self.primary_bg)
        stats_sizer = wx.BoxSizer(wx.VERTICAL)

        stats_title = wx.StaticText(stats_card, label="Quick Stats")
        stats_title.SetFont(
            wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        stats_title.SetForegroundColour(wx.Colour(self.text_dark))

        # Stats grid
        stats_grid = wx.FlexGridSizer(rows=0, cols=2, vgap=15, hgap=15)
        stats_grid.AddGrowableCol(1, 1)

        def add_stat_row(parent, label, value="-"):
            lbl = wx.StaticText(parent, label=label)
            lbl.SetFont(
                wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            lbl.SetForegroundColour(wx.Colour(self.text_muted))

            val = wx.StaticText(parent, label=value)
            val.SetFont(
                wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            val.SetForegroundColour(wx.Colour(self.helen_color))

            return lbl, val

        # Create stat rows
        self.stat_age_label, self.stat_age = add_stat_row(stats_card, "Age:", "-")
        self.stat_height_label, self.stat_height = add_stat_row(stats_card, "Height:", "-")
        self.stat_weight_label, self.stat_weight = add_stat_row(stats_card, "Weight:", "-")
        self.stat_bmi_label, self.stat_bmi = add_stat_row(stats_card, "BMI:", "-")

        stats_grid.AddMany([
            self.stat_age_label, self.stat_age,
            self.stat_height_label, self.stat_height,
            self.stat_weight_label, self.stat_weight,
            self.stat_bmi_label, self.stat_bmi
        ])

        stats_sizer.Add(stats_title, 0, wx.ALL, 15)
        stats_sizer.Add(stats_grid, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        stats_card.SetSizer(stats_sizer)
        left_sizer.Add(stats_card, 0, wx.EXPAND | wx.ALL, 15)

        # Edit Profile Button
        self.edit_profile_btn = wx.Button(left_sidebar, label="✏️ Edit Profile", size=(-1, 50))
        self.edit_profile_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        self.edit_profile_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        self.edit_profile_btn.SetFont(
            wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.edit_profile_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.edit_profile_btn.Bind(wx.EVT_BUTTON, self.on_edit_profile)
        self.edit_profile_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.edit_profile_btn, self.helen_hover)
        )
        self.edit_profile_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.edit_profile_btn, self.helen_color)
        )

        left_sizer.Add(self.edit_profile_btn, 0, wx.EXPAND | wx.ALL, 20)

        # Clear Data Button
        self.clear_data_btn = wx.Button(left_sidebar, label="🧹 Clear My Data", size=(-1, 40))
        self.clear_data_btn.SetBackgroundColour(wx.Colour("#DC3545"))
        self.clear_data_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        self.clear_data_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.clear_data_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.clear_data_btn.Bind(wx.EVT_BUTTON, lambda evt: self.clear_user_data())
        self.clear_data_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.clear_data_btn, "#B02A37")
        )
        self.clear_data_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.clear_data_btn, "#DC3545")
        )

        left_sizer.Add(self.clear_data_btn, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)

        left_sidebar.SetSizer(left_sizer)

        # RIGHT CONTENT - Tabs for different sections
        right_content = wx.Panel(content_panel)
        right_content.SetBackgroundColour(self.card_bg)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        # Notebook for tabs
        self.notebook = wx.Notebook(right_content)

        self.notebook.SetForegroundColour(wx.Colour(self.text_dark))

        # Tab 1: Progress Charts
        self.progress_panel = wx.Panel(self.notebook)
        self.progress_panel.SetBackgroundColour(self.card_bg)
        self.create_progress_tab()

        # Tab 2: Weight Tracking
        self.weight_panel = wx.Panel(self.notebook)
        self.weight_panel.SetBackgroundColour(self.card_bg)
        self.create_weight_tab()

        # Tab 3: Workout History
        self.workout_panel = wx.Panel(self.notebook)
        self.workout_panel.SetBackgroundColour(self.card_bg)
        self.create_workout_tab()

        # Tab 4: Diet History
        self.diet_panel = wx.Panel(self.notebook)
        self.diet_panel.SetBackgroundColour(self.card_bg)
        self.create_diet_tab()

        self.notebook.AddPage(self.progress_panel, "📊 Progress Charts")
        self.notebook.AddPage(self.weight_panel, "⚖️ Weight Tracking")
        self.notebook.AddPage(self.workout_panel, "💪 Workout History")
        self.notebook.AddPage(self.diet_panel, "🥗 Diet History")

        self.set_tab_text_color_black()

        right_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 10)

        right_content.SetSizer(right_sizer)

        # Add to content sizer
        content_sizer.Add(left_sidebar, 0, wx.EXPAND | wx.RIGHT, 15)
        content_sizer.Add(right_content, 1, wx.EXPAND)

        content_panel.SetSizer(content_sizer)
        main_sizer.Add(content_panel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # FOOTER
        footer_panel = wx.Panel(panel)
        footer_panel.SetBackgroundColour(self.primary_bg)
        footer_sizer = wx.BoxSizer(wx.HORIZONTAL)

        copyright_text = wx.StaticText(
            footer_panel,
            label="© 2025 Smart Fitness Assistant. All rights reserved. | Version 1.0.0"
        )
        copyright_text.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        copyright_text.SetForegroundColour(wx.Colour(self.text_muted))

        footer_sizer.Add(copyright_text, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        footer_panel.SetSizer(footer_sizer)
        main_sizer.Add(footer_panel, 0, wx.EXPAND)

        panel.SetSizer(main_sizer)
        self.Centre()

        # Load user profile Dataset
        self.load_user_profile()

        # Load history Dataset
        self.load_weight_history()
        self.load_workout_history()
        self.load_diet_history()

    def set_tab_text_color_black(self):
        """Sets black text for all elements in tabs"""
        self.notebook.SetForegroundColour(wx.Colour(self.text_dark))

        for i in range(self.notebook.GetPageCount()):
            panel = self.notebook.GetPage(i)
            self.set_panel_text_color_black(panel)

    def set_panel_text_color_black(self, panel):
        try:
            panel.SetForegroundColour(wx.Colour(self.text_dark))
        except:
            pass

        for child in panel.GetChildren():
            if isinstance(child, wx.Panel):
                self.set_panel_text_color_black(child)
            else:
                try:
                    child.SetForegroundColour(wx.Colour(self.text_dark))
                except:
                    pass

    def create_progress_tab(self):
        """Create progress charts tab"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title with expand button
        title_panel = wx.Panel(self.progress_panel)
        title_panel.SetBackgroundColour(self.card_bg)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title = wx.StaticText(title_panel, label="Your Progress Over Time")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour(self.text_dark))

        expand_btn = wx.Button(title_panel, label="🔍 Expand Chart", size=(120, 30))
        expand_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        expand_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        expand_btn.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        expand_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        expand_btn.Bind(wx.EVT_BUTTON, self.on_expand_chart)

        title_sizer.Add(title, 1, wx.ALIGN_CENTER_VERTICAL)
        title_sizer.Add(expand_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        title_panel.SetSizer(title_sizer)

        # Create matplotlib figure
        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.progress_panel, -1, self.figure)

        # Date range selector
        range_panel = wx.Panel(self.progress_panel)
        range_panel.SetBackgroundColour(self.card_bg)
        range_sizer = wx.BoxSizer(wx.HORIZONTAL)

        range_label = wx.StaticText(range_panel, label="Show:")
        range_label.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        range_label.SetForegroundColour(wx.Colour(self.text_dark))

        self.range_choice = wx.ComboBox(
            range_panel,
            choices=["Last 7 days", "Last 30 days", "Last 3 months", "All time"],
            style=wx.CB_READONLY
        )
        self.range_choice.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.range_choice.SetForegroundColour(wx.Colour(self.text_dark))
        self.range_choice.SetSelection(1)
        self.range_choice.Bind(wx.EVT_COMBOBOX, self.on_range_change)

        range_sizer.Add(range_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        range_sizer.Add(self.range_choice, 0)

        range_panel.SetSizer(range_sizer)

        main_sizer.Add(title_panel, 0, wx.EXPAND | wx.ALL, 15)
        main_sizer.Add(self.canvas, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        main_sizer.Add(range_panel, 0, wx.ALIGN_RIGHT | wx.ALL, 15)

        self.progress_panel.SetSizer(main_sizer)

        # Update chart after creating range_choice
        self.update_progress_chart()

    def create_weight_tab(self):
        """Create weight tracking tab"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title with expand button
        title_panel = wx.Panel(self.weight_panel)
        title_panel.SetBackgroundColour(self.card_bg)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title = wx.StaticText(title_panel, label="Track Your Weight")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour(self.text_dark))

        expand_btn = wx.Button(title_panel, label="📋 View Full History", size=(150, 30))
        expand_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        expand_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        expand_btn.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        expand_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        expand_btn.Bind(wx.EVT_BUTTON, self.on_expand_weight)

        title_sizer.Add(title, 1, wx.ALIGN_CENTER_VERTICAL)
        title_sizer.Add(expand_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        title_panel.SetSizer(title_sizer)

        # Add weight entry form
        entry_panel = wx.Panel(self.weight_panel)
        entry_panel.SetBackgroundColour(self.primary_bg)
        entry_sizer = wx.BoxSizer(wx.VERTICAL)

        # Form fields in horizontal sizer
        fields_sizer = wx.BoxSizer(wx.HORIZONTAL)

        weight_label = wx.StaticText(entry_panel, label="Weight (kg):")
        weight_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        weight_label.SetForegroundColour(wx.Colour(self.text_dark))

        self.new_weight = wx.TextCtrl(entry_panel, size=(100, 35))
        self.new_weight.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.new_weight.SetForegroundColour(wx.Colour(self.text_dark))

        notes_label = wx.StaticText(entry_panel, label="Notes:")
        notes_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        notes_label.SetForegroundColour(wx.Colour(self.text_dark))

        self.weight_notes = wx.TextCtrl(entry_panel, size=(200, 35))
        self.weight_notes.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.weight_notes.SetForegroundColour(wx.Colour(self.text_dark))

        fields_sizer.Add(weight_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        fields_sizer.Add(self.new_weight, 0, wx.RIGHT, 20)
        fields_sizer.Add(notes_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        fields_sizer.Add(self.weight_notes, 1, wx.RIGHT, 20)

        entry_sizer.Add(fields_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 15)

        # Add button
        add_btn = wx.Button(entry_panel, label="Add Entry", size=(150, 40))
        add_btn.SetBackgroundColour(wx.Colour(self.accent_green))
        add_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        add_btn.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        add_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_weight)
        add_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, add_btn, self.green_hover)
        )
        add_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, add_btn, self.accent_green)
        )

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(add_btn, 0, wx.ALIGN_CENTER)
        entry_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 15)

        entry_panel.SetSizer(entry_sizer)

        # Weight history list
        history_label = wx.StaticText(self.weight_panel, label="Recent Weight History")
        history_label.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        history_label.SetForegroundColour(wx.Colour(self.text_dark))

        # Create list control for weight history
        self.weight_list = wx.ListCtrl(
            self.weight_panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.weight_list.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.weight_list.SetForegroundColour(wx.Colour(self.text_dark))
        self.weight_list.SetTextColour(wx.Colour(self.text_dark))
        self.weight_list.AppendColumn("Date", width=150)
        self.weight_list.AppendColumn("Weight (kg)", width=100)
        self.weight_list.AppendColumn("Notes", width=300)

        # Double-click to view details
        self.weight_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_view_weight_detail)

        main_sizer.Add(title_panel, 0, wx.EXPAND | wx.ALL, 15)
        main_sizer.Add(entry_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        main_sizer.AddSpacer(20)
        main_sizer.Add(history_label, 0, wx.LEFT | wx.RIGHT, 15)
        main_sizer.Add(self.weight_list, 1, wx.EXPAND | wx.ALL, 15)

        self.weight_panel.SetSizer(main_sizer)

    def create_workout_tab(self):
        """Create workout history tab"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title with expand button
        title_panel = wx.Panel(self.workout_panel)
        title_panel.SetBackgroundColour(self.card_bg)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title = wx.StaticText(title_panel, label="Workout History")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour(self.text_dark))

        expand_btn = wx.Button(title_panel, label="📋 View Full History", size=(150, 30))
        expand_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        expand_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        expand_btn.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        expand_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        expand_btn.Bind(wx.EVT_BUTTON, self.on_expand_workout)

        title_sizer.Add(title, 1, wx.ALIGN_CENTER_VERTICAL)
        title_sizer.Add(expand_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        title_panel.SetSizer(title_sizer)

        # Add workout entry form
        entry_panel = wx.Panel(self.workout_panel)
        entry_panel.SetBackgroundColour(self.primary_bg)
        entry_sizer = wx.BoxSizer(wx.VERTICAL)

        # Form title
        form_title = wx.StaticText(entry_panel, label="Add New Workout")
        form_title.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        form_title.SetForegroundColour(wx.Colour(self.text_dark))

        # Workout type row
        type_sizer = wx.BoxSizer(wx.HORIZONTAL)
        type_label = wx.StaticText(entry_panel, label="Workout type:")
        type_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        type_label.SetForegroundColour(wx.Colour(self.text_dark))
        type_label.SetMinSize((120, -1))

        self.workout_type = wx.ComboBox(
            entry_panel,
            choices=["Cardio", "Strength", "HIIT", "Yoga", "Swimming", "Cycling", "Walking", "Other"],
            style=wx.CB_READONLY,
            size=(200, 35)
        )
        self.workout_type.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.workout_type.SetForegroundColour(wx.Colour(self.text_dark))
        self.workout_type.SetSelection(0)

        type_sizer.Add(type_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        type_sizer.Add(self.workout_type, 1, wx.EXPAND)

        # Duration row
        duration_sizer = wx.BoxSizer(wx.HORIZONTAL)
        duration_label = wx.StaticText(entry_panel, label="Duration (minutes):")
        duration_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        duration_label.SetForegroundColour(wx.Colour(self.text_dark))
        duration_label.SetMinSize((120, -1))

        self.workout_duration = wx.TextCtrl(entry_panel, size=(200, 35))
        self.workout_duration.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.workout_duration.SetForegroundColour(wx.Colour(self.text_dark))

        duration_sizer.Add(duration_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        duration_sizer.Add(self.workout_duration, 1, wx.EXPAND)

        # Calories burned row
        calories_sizer = wx.BoxSizer(wx.HORIZONTAL)
        calories_label = wx.StaticText(entry_panel, label="Calories Burned:")
        calories_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        calories_label.SetForegroundColour(wx.Colour(self.text_dark))
        calories_label.SetMinSize((120, -1))

        self.workout_calories = wx.TextCtrl(entry_panel, size=(200, 35))
        self.workout_calories.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.workout_calories.SetForegroundColour(wx.Colour(self.text_dark))

        calories_sizer.Add(calories_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        calories_sizer.Add(self.workout_calories, 1, wx.EXPAND)

        # Notes row
        notes_sizer = wx.BoxSizer(wx.HORIZONTAL)
        notes_label = wx.StaticText(entry_panel, label="Notes:")
        notes_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        notes_label.SetForegroundColour(wx.Colour(self.text_dark))
        notes_label.SetMinSize((120, -1))

        self.workout_notes = wx.TextCtrl(entry_panel, size=(200, 35))
        self.workout_notes.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.workout_notes.SetForegroundColour(wx.Colour(self.text_dark))

        notes_sizer.Add(notes_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        notes_sizer.Add(self.workout_notes, 1, wx.EXPAND)

        # Add all to entry_sizer
        entry_sizer.Add(form_title, 0, wx.ALL, 10)
        entry_sizer.Add(type_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        entry_sizer.Add(duration_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        entry_sizer.Add(calories_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        entry_sizer.Add(notes_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # Add button
        add_btn = wx.Button(entry_panel, label="Add Workout", size=(150, 45))
        add_btn.SetBackgroundColour(wx.Colour(self.accent_green))
        add_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        add_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        add_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_workout)
        add_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, add_btn, self.green_hover)
        )
        add_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, add_btn, self.accent_green)
        )

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(add_btn, 0, wx.ALIGN_CENTER)
        entry_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 15)

        entry_panel.SetSizer(entry_sizer)

        # Separator
        separator = wx.StaticLine(self.workout_panel, style=wx.LI_HORIZONTAL, size=(-1, 2))
        separator.SetBackgroundColour(wx.Colour(self.border))

        # History title
        history_title = wx.StaticText(self.workout_panel, label="Recent Workout History")
        history_title.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        history_title.SetForegroundColour(wx.Colour(self.text_dark))

        # Workout history list
        self.workout_list = wx.ListCtrl(
            self.workout_panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.workout_list.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.workout_list.SetForegroundColour(wx.Colour(self.text_dark))
        self.workout_list.SetTextColour(wx.Colour(self.text_dark))
        self.workout_list.AppendColumn("Date", width=150)
        self.workout_list.AppendColumn("Type", width=100)
        self.workout_list.AppendColumn("Duration", width=80)
        self.workout_list.AppendColumn("Calories", width=80)
        self.workout_list.AppendColumn("Notes", width=200)

        # Double-click to view details
        self.workout_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_view_workout_detail)

        main_sizer.Add(title_panel, 0, wx.EXPAND | wx.ALL, 15)
        main_sizer.Add(entry_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        main_sizer.Add(separator, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 15)
        main_sizer.Add(history_title, 0, wx.LEFT | wx.RIGHT, 15)
        main_sizer.Add(self.workout_list, 1, wx.EXPAND | wx.ALL, 15)

        self.workout_panel.SetSizer(main_sizer)

    def create_diet_tab(self):
        """Create diet history tab"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title with expand button
        title_panel = wx.Panel(self.diet_panel)
        title_panel.SetBackgroundColour(self.card_bg)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title = wx.StaticText(title_panel, label="Diet History")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour(self.text_dark))

        expand_btn = wx.Button(title_panel, label="📋 View Full History", size=(150, 30))
        expand_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        expand_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        expand_btn.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        expand_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        expand_btn.Bind(wx.EVT_BUTTON, self.on_expand_diet)

        title_sizer.Add(title, 1, wx.ALIGN_CENTER_VERTICAL)
        title_sizer.Add(expand_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        title_panel.SetSizer(title_sizer)

        # Add diet entry form
        entry_panel = wx.Panel(self.diet_panel)
        entry_panel.SetBackgroundColour(self.primary_bg)
        entry_sizer = wx.BoxSizer(wx.VERTICAL)

        # Form title
        form_title = wx.StaticText(entry_panel, label="Add New Meal")
        form_title.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        form_title.SetForegroundColour(wx.Colour(self.text_dark))

        # Meal type row
        type_sizer = wx.BoxSizer(wx.HORIZONTAL)
        type_label = wx.StaticText(entry_panel, label="Meal type:")
        type_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        type_label.SetForegroundColour(wx.Colour(self.text_dark))
        type_label.SetMinSize((120, -1))

        self.meal_type = wx.ComboBox(
            entry_panel,
            choices=["Breakfast", "Lunch", "Dinner", "Snack", "Protein Intake", "Other"],
            style=wx.CB_READONLY,
            size=(200, 35)
        )
        self.meal_type.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.meal_type.SetForegroundColour(wx.Colour(self.text_dark))
        self.meal_type.SetSelection(0)

        type_sizer.Add(type_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        type_sizer.Add(self.meal_type, 1, wx.EXPAND)

        # Calories row
        calories_sizer = wx.BoxSizer(wx.HORIZONTAL)
        calories_label = wx.StaticText(entry_panel, label="Calories:")
        calories_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        calories_label.SetForegroundColour(wx.Colour(self.text_dark))
        calories_label.SetMinSize((120, -1))

        self.meal_calories = wx.TextCtrl(entry_panel, size=(200, 35))
        self.meal_calories.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.meal_calories.SetForegroundColour(wx.Colour(self.text_dark))
        self.meal_calories.SetHint("kcal")

        calories_sizer.Add(calories_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        calories_sizer.Add(self.meal_calories, 1, wx.EXPAND)

        # Protein row
        protein_sizer = wx.BoxSizer(wx.HORIZONTAL)
        protein_label = wx.StaticText(entry_panel, label="Protein (g):")
        protein_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        protein_label.SetForegroundColour(wx.Colour(self.text_dark))
        protein_label.SetMinSize((120, -1))

        self.meal_protein = wx.TextCtrl(entry_panel, size=(200, 35))
        self.meal_protein.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.meal_protein.SetForegroundColour(wx.Colour(self.text_dark))
        self.meal_protein.SetHint("grams")

        protein_sizer.Add(protein_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        protein_sizer.Add(self.meal_protein, 1, wx.EXPAND)

        # Carbs row
        carbs_sizer = wx.BoxSizer(wx.HORIZONTAL)
        carbs_label = wx.StaticText(entry_panel, label="Carbs (g):")
        carbs_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        carbs_label.SetForegroundColour(wx.Colour(self.text_dark))
        carbs_label.SetMinSize((120, -1))

        self.meal_carbs = wx.TextCtrl(entry_panel, size=(200, 35))
        self.meal_carbs.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.meal_carbs.SetForegroundColour(wx.Colour(self.text_dark))
        self.meal_carbs.SetHint("grams")

        carbs_sizer.Add(carbs_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        carbs_sizer.Add(self.meal_carbs, 1, wx.EXPAND)

        # Fats row
        fats_sizer = wx.BoxSizer(wx.HORIZONTAL)
        fats_label = wx.StaticText(entry_panel, label="Fats (g):")
        fats_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        fats_label.SetForegroundColour(wx.Colour(self.text_dark))
        fats_label.SetMinSize((120, -1))

        self.meal_fats = wx.TextCtrl(entry_panel, size=(200, 35))
        self.meal_fats.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.meal_fats.SetForegroundColour(wx.Colour(self.text_dark))
        self.meal_fats.SetHint("grams")

        fats_sizer.Add(fats_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        fats_sizer.Add(self.meal_fats, 1, wx.EXPAND)

        # Notes row
        notes_sizer = wx.BoxSizer(wx.HORIZONTAL)
        notes_label = wx.StaticText(entry_panel, label="Notes:")
        notes_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        notes_label.SetForegroundColour(wx.Colour(self.text_dark))
        notes_label.SetMinSize((120, -1))

        self.meal_notes = wx.TextCtrl(entry_panel, size=(200, 35))
        self.meal_notes.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.meal_notes.SetForegroundColour(wx.Colour(self.text_dark))
        self.meal_notes.SetHint("Optional")

        notes_sizer.Add(notes_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        notes_sizer.Add(self.meal_notes, 1, wx.EXPAND)

        # Add all to entry_sizer
        entry_sizer.Add(form_title, 0, wx.ALL, 10)
        entry_sizer.Add(type_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        entry_sizer.Add(calories_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        entry_sizer.Add(protein_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        entry_sizer.Add(carbs_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        entry_sizer.Add(fats_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        entry_sizer.Add(notes_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # Add button
        add_btn = wx.Button(entry_panel, label="Add Meal", size=(150, 45))
        add_btn.SetBackgroundColour(wx.Colour(self.accent_green))
        add_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        add_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        add_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_meal)
        add_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, add_btn, self.green_hover)
        )
        add_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, add_btn, self.accent_green)
        )

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(add_btn, 0, wx.ALIGN_CENTER)
        entry_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 15)

        entry_panel.SetSizer(entry_sizer)

        # Separator
        separator = wx.StaticLine(self.diet_panel, style=wx.LI_HORIZONTAL, size=(-1, 2))
        separator.SetBackgroundColour(wx.Colour(self.border))

        # Today's summary
        summary_panel = wx.Panel(self.diet_panel)
        summary_panel.SetBackgroundColour(self.primary_bg)
        summary_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.today_calories = wx.StaticText(summary_panel, label="Today: 0 kcal")
        self.today_calories.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.today_calories.SetForegroundColour(wx.Colour(self.helen_color))

        self.today_protein = wx.StaticText(summary_panel, label="Protein: 0g")
        self.today_protein.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.today_protein.SetForegroundColour(wx.Colour(self.accent_green))

        self.today_carbs = wx.StaticText(summary_panel, label="Carbs: 0g")
        self.today_carbs.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.today_carbs.SetForegroundColour(wx.Colour(self.helen_hover))

        self.today_fats = wx.StaticText(summary_panel, label="Fats: 0g")
        self.today_fats.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.today_fats.SetForegroundColour(wx.Colour(self.text_dark))

        summary_sizer.Add(self.today_calories, 0, wx.RIGHT, 20)
        summary_sizer.Add(self.today_protein, 0, wx.RIGHT, 20)
        summary_sizer.Add(self.today_carbs, 0, wx.RIGHT, 20)
        summary_sizer.Add(self.today_fats, 0)

        summary_panel.SetSizer(summary_sizer)

        # Diet history list
        history_title = wx.StaticText(self.diet_panel, label="Recent Diet History")
        history_title.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        history_title.SetForegroundColour(wx.Colour(self.text_dark))

        self.diet_list = wx.ListCtrl(
            self.diet_panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.diet_list.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.diet_list.SetForegroundColour(wx.Colour(self.text_dark))
        self.diet_list.SetTextColour(wx.Colour(self.text_dark))
        self.diet_list.AppendColumn("Date", width=150)
        self.diet_list.AppendColumn("Meal", width=100)
        self.diet_list.AppendColumn("Calories", width=80)
        self.diet_list.AppendColumn("Protein", width=80)
        self.diet_list.AppendColumn("Carbs", width=80)
        self.diet_list.AppendColumn("Fats", width=80)
        self.diet_list.AppendColumn("Notes", width=150)

        # Double-click to view details
        self.diet_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_view_diet_detail)

        main_sizer.Add(title_panel, 0, wx.EXPAND | wx.ALL, 15)
        main_sizer.Add(entry_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        main_sizer.Add(separator, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 15)
        main_sizer.Add(summary_panel, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        main_sizer.Add(history_title, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        main_sizer.Add(self.diet_list, 1, wx.EXPAND | wx.ALL, 15)

        self.diet_panel.SetSizer(main_sizer)

    # Methods for expanding views
    def on_expand_chart(self, event):
        """Open expanded chart window"""
        dialog = ExpandedChartDialog(self, self.current_user)
        dialog.ShowModal()
        dialog.Destroy()

    def on_expand_weight(self, event):
        """Open expanded weight history window"""
        dialog = ExpandedWeightDialog(self, self.current_user)
        dialog.ShowModal()
        dialog.Destroy()

    def on_expand_workout(self, event):
        """Open expanded workout history window"""
        dialog = ExpandedWorkoutDialog(self, self.current_user)
        dialog.ShowModal()
        dialog.Destroy()

    def on_expand_diet(self, event):
        """Open expanded diet history window"""
        dialog = ExpandedDietDialog(self, self.current_user)
        dialog.ShowModal()
        dialog.Destroy()

    def on_view_weight_detail(self, event):
        """View weight entry details"""
        index = event.GetIndex()
        date = self.weight_list.GetItemText(index)
        weight = self.weight_list.GetItem(index, 1).GetText()
        notes = self.weight_list.GetItem(index, 2).GetText()

        dialog = DetailViewDialog(self, "Weight Entry Details",
                                  f"Date: {date}\nWeight: {weight} kg\nNotes: {notes}")
        dialog.ShowModal()
        dialog.Destroy()

    def on_view_workout_detail(self, event):
        """View workout entry details"""
        index = event.GetIndex()
        date = self.workout_list.GetItemText(index)
        wtype = self.workout_list.GetItem(index, 1).GetText()
        duration = self.workout_list.GetItem(index, 2).GetText()
        calories = self.workout_list.GetItem(index, 3).GetText()
        notes = self.workout_list.GetItem(index, 4).GetText()

        dialog = DetailViewDialog(self, "Workout Entry Details",
                                  f"Date: {date}\nType: {wtype}\nDuration: {duration} min\nCalories Burned: {calories}\nNotes: {notes}")
        dialog.ShowModal()
        dialog.Destroy()

    def on_view_diet_detail(self, event):
        """View diet entry details"""
        index = event.GetIndex()
        date = self.diet_list.GetItemText(index)
        meal = self.diet_list.GetItem(index, 1).GetText()
        calories = self.diet_list.GetItem(index, 2).GetText()
        protein = self.diet_list.GetItem(index, 3).GetText()
        carbs = self.diet_list.GetItem(index, 4).GetText()
        fats = self.diet_list.GetItem(index, 5).GetText()
        notes = self.diet_list.GetItem(index, 6).GetText()

        dialog = DetailViewDialog(self, "Meal Entry Details",
                                  f"Date: {date}\nMeal: {meal}\nCalories: {calories} kcal\nProtein: {protein}g\nCarbs: {carbs}g\nFats: {fats}g\nNotes: {notes}")
        dialog.ShowModal()
        dialog.Destroy()

    def on_add_meal(self, event):
        """Handle adding a new meal entry"""
        if not self.current_user:
            wx.MessageBox("User not logged in!", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Get values from form
        meal_type = self.meal_type.GetValue()
        calories = self.meal_calories.GetValue().strip()
        protein = self.meal_protein.GetValue().strip()
        carbs = self.meal_carbs.GetValue().strip()
        fats = self.meal_fats.GetValue().strip()
        notes = self.meal_notes.GetValue().strip()

        # Validate required fields
        if not meal_type or not calories:
            wx.MessageBox("Please fill in meal type and calories", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            # Convert to numbers (allow empty values to become 0)
            calories_val = int(calories) if calories else 0
            protein_val = int(protein) if protein else 0
            carbs_val = int(carbs) if carbs else 0
            fats_val = int(fats) if fats else 0

            # Insert into database
            self.cursor.execute(
                """INSERT INTO diet_history 
                   (user_id, meal_type, calories, protein, carbs, fats, notes, date) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                (self.current_user['id'], meal_type, calories_val, protein_val,
                 carbs_val, fats_val, notes)
            )
            self.conn.commit()

            # Clear form fields
            self.meal_calories.SetValue("")
            self.meal_protein.SetValue("")
            self.meal_carbs.SetValue("")
            self.meal_fats.SetValue("")
            self.meal_notes.SetValue("")
            self.meal_type.SetSelection(0)

            # Refresh the diet history list and today's summary
            self.load_diet_history()

            wx.MessageBox("Meal added successfully!", "Success", wx.OK | wx.ICON_INFORMATION)

        except ValueError:
            wx.MessageBox("Please enter valid numbers for calories and macros",
                          "Error", wx.OK | wx.ICON_ERROR)
        except sqlite3.Error as e:
            wx.MessageBox(f"Dataset error: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def load_user_profile(self):
        """Load user profile Dataset from database - only from Edit Profile"""
        if not self.current_user:
            return

        try:
            self.cursor.execute(
                "SELECT age, height, weight FROM user_profiles WHERE user_id = ?",
                (self.current_user['id'],)
            )
            profile = self.cursor.fetchone()

            if profile:
                age, height, weight = profile

                # Update stats display
                self.stat_age.SetLabel(str(age) if age else "-")
                self.stat_height.SetLabel(f"{height} m" if height else "-")
                self.stat_weight.SetLabel(f"{weight} kg" if weight else "-")

                # Calculate BMI if height and weight available
                if height and weight:
                    bmi = weight / (height ** 2)
                    self.stat_bmi.SetLabel(f"{bmi:.1f}")
                else:
                    self.stat_bmi.SetLabel("-")
            else:
                self.stat_age.SetLabel("-")
                self.stat_height.SetLabel("-")
                self.stat_weight.SetLabel("-")
                self.stat_bmi.SetLabel("-")

        except sqlite3.Error as e:
            print(f"Error loading profile: {e}")
            self.stat_age.SetLabel("-")
            self.stat_height.SetLabel("-")
            self.stat_weight.SetLabel("-")
            self.stat_bmi.SetLabel("-")

    def load_weight_history(self):
        """Load weight history from database for current user"""
        if not self.current_user:
            return

        self.weight_list.DeleteAllItems()

        try:
            self.cursor.execute(
                "SELECT date, weight, notes FROM weight_history WHERE user_id = ? ORDER BY date DESC LIMIT 20",
                (self.current_user['id'],)
            )
            records = self.cursor.fetchall()

            for i, (date, weight, notes) in enumerate(records):
                if isinstance(date, str):
                    date_str = date[:10]
                else:
                    date_str = str(date)

                index = self.weight_list.InsertItem(i, date_str)
                self.weight_list.SetItem(index, 1, f"{weight:.1f}")
                self.weight_list.SetItem(index, 2, notes if notes else "")

        except sqlite3.Error as e:
            print(f"Error loading weight history: {e}")

    def load_workout_history(self):
        """Load workout history from database for current user"""
        if not self.current_user:
            return

        self.workout_list.DeleteAllItems()

        try:
            self.cursor.execute(
                "SELECT date, workout_type, duration, calories_burned, notes FROM workout_history WHERE user_id = ? ORDER BY date DESC LIMIT 20",
                (self.current_user['id'],)
            )
            records = self.cursor.fetchall()

            for i, (date, wtype, duration, calories, notes) in enumerate(records):
                if isinstance(date, str):
                    date_str = date[:10]
                else:
                    date_str = str(date)

                index = self.workout_list.InsertItem(i, date_str)
                self.workout_list.SetItem(index, 1, wtype)
                self.workout_list.SetItem(index, 2, str(duration))
                self.workout_list.SetItem(index, 3, str(calories))
                self.workout_list.SetItem(index, 4, notes if notes else "")

        except sqlite3.Error as e:
            print(f"Error loading workout history: {e}")

    def load_diet_history(self):
        """Load diet history from database for current user"""
        if not self.current_user:
            return

        self.diet_list.DeleteAllItems()

        try:
            self.cursor.execute(
                "SELECT date, meal_type, calories, protein, carbs, fats, notes FROM diet_history WHERE user_id = ? ORDER BY date DESC LIMIT 20",
                (self.current_user['id'],)
            )
            records = self.cursor.fetchall()

            for i, (date, meal, cal, protein, carbs, fats, notes) in enumerate(records):
                if isinstance(date, str):
                    date_str = date[:10]
                else:
                    date_str = str(date)

                index = self.diet_list.InsertItem(i, date_str)
                self.diet_list.SetItem(index, 1, meal)
                self.diet_list.SetItem(index, 2, str(cal))
                self.diet_list.SetItem(index, 3, str(protein))
                self.diet_list.SetItem(index, 4, str(carbs))
                self.diet_list.SetItem(index, 5, str(fats))
                self.diet_list.SetItem(index, 6, notes if notes else "")

            self.update_today_summary()

        except sqlite3.Error as e:
            print(f"Error loading diet history: {e}")

    def update_today_summary(self):
        """Update today's nutrition summary"""
        if not self.current_user:
            return

        try:
            today = datetime.now().strftime('%Y-%m-%d')
            self.cursor.execute(
                """SELECT SUM(calories), SUM(protein), SUM(carbs), SUM(fats) 
                   FROM diet_history 
                   WHERE user_id = ? AND date LIKE ?""",
                (self.current_user['id'], f'{today}%')
            )
            result = self.cursor.fetchone()

            if result and result[0]:
                total_cal, total_protein, total_carbs, total_fats = result
                self.today_calories.SetLabel(f"Today: {total_cal or 0} kcal")
                self.today_protein.SetLabel(f"Protein: {total_protein or 0}g")
                self.today_carbs.SetLabel(f"Carbs: {total_carbs or 0}g")
                self.today_fats.SetLabel(f"Fats: {total_fats or 0}g")
            else:
                self.today_calories.SetLabel("Today: 0 kcal")
                self.today_protein.SetLabel("Protein: 0g")
                self.today_carbs.SetLabel("Carbs: 0g")
                self.today_fats.SetLabel("Fats: 0g")

        except sqlite3.Error as e:
            print(f"Error updating today's summary: {e}")

    def update_progress_chart(self):
        """Update the progress chart with real Dataset"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if self.current_user:
            try:
                # Get weight history for chart
                range_map = {
                    "Last 7 days": 7,
                    "Last 30 days": 30,
                    "Last 3 months": 90,
                    "All time": None
                }

                # Check if range_choice exists
                if self.range_choice:
                    days = range_map.get(self.range_choice.GetValue(), 7)
                else:
                    days = 7  # Default value

                if days:
                    self.cursor.execute(
                        "SELECT date, weight FROM weight_history WHERE user_id = ? AND date >= date('now', ?) ORDER BY date",
                        (self.current_user['id'], f'-{days} days')
                    )
                else:
                    self.cursor.execute(
                        "SELECT date, weight FROM weight_history WHERE user_id = ? ORDER BY date",
                        (self.current_user['id'],)
                    )
                weights = self.cursor.fetchall()

                if weights:
                    dates = [w[0][5:10] if isinstance(w[0], str) else str(w[0]) for w in weights]
                    weight_values = [w[1] for w in weights]

                    ax.plot(dates, weight_values, 'b-o', label='Weight (kg)', linewidth=2, markersize=8)
                    ax.set_xlabel('Date')
                    ax.set_ylabel('Weight (kg)', color='b')
                    ax.tick_params(axis='y', labelcolor='b')
                    ax.grid(True, alpha=0.3)
                    ax.set_title('Weight Progress Over Time', fontsize=12, fontweight='bold')

                    # Rotate x-axis labels for better readability
                    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
                else:
                    ax.text(0.5, 0.5, 'No weight Dataset available', ha='center', va='center', transform=ax.transAxes,
                            fontsize=12, color=self.text_dark)

            except sqlite3.Error as e:
                print(f"Error loading chart Dataset: {e}")
                ax.text(0.5, 0.5, 'Error loading Dataset', ha='center', va='center', transform=ax.transAxes,
                        fontsize=12, color=self.text_dark)
        else:
            ax.text(0.5, 0.5, 'No user logged in', ha='center', va='center', transform=ax.transAxes,
                    fontsize=12, color=self.text_dark)

        self.figure.tight_layout()
        self.canvas.draw()

    def clear_user_data(self):
        """Clear all Dataset for the current unser"""
        if not self.current_user:
            wx.MessageBox("Could not find logged in user", "Error", wx.OK | wx.ICON_ERROR)
            return

        dlg = wx.MessageDialog(self,
                               "This will delete all your Dataset about:\n\n" +
                               "• Weight\n" +
                               "• Exercises\n" +
                               "• Diets\n\n" +
                               "Are you sure you want to continue?\n\n" +
                               "(This action cannot be reverted!)",
                               "Clear all Dataset",
                               wx.YES_NO | wx.ICON_WARNING)

        if dlg.ShowModal() == wx.ID_YES:
            try:
                self.cursor.execute("DELETE FROM weight_history WHERE user_id = ?", (self.current_user['id'],))
                weight_count = self.cursor.rowcount

                self.cursor.execute("DELETE FROM workout_history WHERE user_id = ?", (self.current_user['id'],))
                workout_count = self.cursor.rowcount

                self.cursor.execute("DELETE FROM diet_history WHERE user_id = ?", (self.current_user['id'],))
                diet_count = self.cursor.rowcount

                self.conn.commit()

                self.load_weight_history()
                self.load_workout_history()
                self.load_diet_history()
                self.update_progress_chart()

                wx.MessageBox(f"Your Dataset was cleared!\n\n" +
                              f"• Deleted Dataset for weight: {weight_count}\n" +
                              f"• Deleted exercises: {workout_count}\n" +
                              f"• Deleted diets: {diet_count}",
                              "Good Luck", wx.OK | wx.ICON_INFORMATION)

            except sqlite3.Error as e:
                wx.MessageBox(f"Error while clearing Dataset: {e}", "Error", wx.OK | wx.ICON_ERROR)

        dlg.Destroy()

    def on_button_hover(self, event, button, color):
        button.SetBackgroundColour(wx.Colour(color))
        button.Refresh()
        event.Skip()

    def on_button_leave(self, event, button, color):
        button.SetBackgroundColour(wx.Colour(color))
        button.Refresh()
        event.Skip()

    def on_home(self, event):
        try:
            from UI.program_GUI import FitnessApp
            main_app = FitnessApp(None, user=self.current_user)
            main_app.Show()
            self.Close()
        except ImportError as e:
            wx.MessageBox(f"Could not open main app: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_logout(self, event):
        try:
            from UI.login_GUI import LoginApp
            login_app = LoginApp(None)
            login_app.Show()
            self.Close()
        except ImportError:
            self.Close()

    def on_edit_profile(self, event):
        dlg = EditProfileDialog(self, title="Edit Profile", user=self.current_user)
        if dlg.ShowModal() == wx.ID_OK:
            # Refresh profile Dataset
            self.load_user_profile()
        dlg.Destroy()

    def on_range_change(self, event):
        self.update_progress_chart()

    def on_add_weight(self, event):
        if not self.current_user:
            wx.MessageBox("User not logged in!", "Error", wx.OK | wx.ICON_ERROR)
            return

        weight = self.new_weight.GetValue().strip()
        notes = self.weight_notes.GetValue().strip()

        if not weight:
            wx.MessageBox("Please enter weight value", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            weight_val = float(weight)

            self.cursor.execute(
                "INSERT INTO weight_history (user_id, weight, notes, date) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                (self.current_user['id'], weight_val, notes)
            )
            self.conn.commit()

            self.new_weight.SetValue("")
            self.weight_notes.SetValue("")

            self.load_weight_history()
            self.update_progress_chart()

            wx.MessageBox("Weight entry added successfully!", "Success", wx.OK | wx.ICON_INFORMATION)

        except ValueError:
            wx.MessageBox("Please enter a valid number for weight", "Error", wx.OK | wx.ICON_ERROR)
        except sqlite3.Error as e:
            wx.MessageBox(f"Dataset error: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_add_workout(self, event):
        if not self.current_user:
            wx.MessageBox("User not logged in!", "Error", wx.OK | wx.ICON_ERROR)
            return

        workout_type = self.workout_type.GetValue()
        duration = self.workout_duration.GetValue().strip()
        calories = self.workout_calories.GetValue().strip()
        notes = self.workout_notes.GetValue().strip()

        if not workout_type or not duration:
            wx.MessageBox("Please fill in required fields", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            duration_val = int(duration)
            calories_val = int(calories) if calories else 0

            self.cursor.execute(
                """INSERT INTO workout_history 
                   (user_id, workout_type, duration, calories_burned, notes, date) 
                   VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                (self.current_user['id'], workout_type, duration_val, calories_val, notes)
            )
            self.conn.commit()

            self.workout_duration.SetValue("")
            self.workout_calories.SetValue("")
            self.workout_notes.SetValue("")

            self.load_workout_history()
            self.update_progress_chart()

            wx.MessageBox("Workout added successfully!", "Success", wx.OK | wx.ICON_INFORMATION)

        except ValueError:
            wx.MessageBox("Please enter valid numbers for duration and calories", "Error", wx.OK | wx.ICON_ERROR)
        except sqlite3.Error as e:
            wx.MessageBox(f"Dataset error: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()


class ExpandedChartDialog(wx.Dialog):
    """Dialog for expanded chart view"""

    def __init__(self, parent, user):
        super(ExpandedChartDialog, self).__init__(parent, title="Progress Chart - Full View", size=(1000, 700))
        self.user = user
        self.parent = parent

        self.SetBackgroundColour(parent.card_bg)
        self.InitUI()

    def InitUI(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create larger figure
        self.figure = plt.Figure(figsize=(12, 8), dpi=100)
        self.canvas = FigureCanvas(self, -1, self.figure)

        # Load and display chart
        self.update_chart()

        # Close button
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_btn = wx.Button(self, label="Close", size=(100, 35))
        close_btn.SetBackgroundColour(wx.Colour(self.parent.helen_color))
        close_btn.SetForegroundColour(wx.Colour(self.parent.button_text_color))
        close_btn.Bind(wx.EVT_BUTTON, lambda evt: self.Close())

        btn_sizer.Add(close_btn, 0, wx.ALIGN_CENTER)

        main_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        self.SetSizer(main_sizer)
        self.Centre()

    def update_chart(self):
        """Update the chart with Dataset"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if self.user:
            try:
                conn = sqlite3.connect('./Database/fitness_app.db')
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT date, weight FROM weight_history WHERE user_id = ? ORDER BY date",
                    (self.user['id'],)
                )
                weights = cursor.fetchall()

                if weights:
                    dates = [w[0][5:10] if isinstance(w[0], str) else str(w[0]) for w in weights]
                    weight_values = [w[1] for w in weights]

                    ax.plot(dates, weight_values, 'b-o', label='Weight (kg)', linewidth=2, markersize=8)
                    ax.set_xlabel('Date', fontsize=12)
                    ax.set_ylabel('Weight (kg)', fontsize=12, color='b')
                    ax.tick_params(axis='y', labelcolor='b')
                    ax.grid(True, alpha=0.3)
                    ax.set_title('Weight Progress Over Time', fontsize=14, fontweight='bold')

                    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
                else:
                    ax.text(0.5, 0.5, 'No weight Dataset available', ha='center', va='center', transform=ax.transAxes,
                            fontsize=14, color='gray')

                conn.close()

            except Exception as e:
                ax.text(0.5, 0.5, f'Error loading Dataset: {e}', ha='center', va='center', transform=ax.transAxes,
                        fontsize=12, color='red')
        else:
            ax.text(0.5, 0.5, 'No user logged in', ha='center', va='center', transform=ax.transAxes,
                    fontsize=14, color='gray')

        self.figure.tight_layout()
        self.canvas.draw()


class ExpandedWeightDialog(wx.Dialog):
    """Dialog for expanded weight history"""

    def __init__(self, parent, user):
        super(ExpandedWeightDialog, self).__init__(parent, title="Weight History - Full View", size=(800, 600))
        self.user = user
        self.parent = parent

        self.SetBackgroundColour(parent.card_bg)
        self.InitUI()

    def InitUI(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create list control for all weight history
        self.weight_list = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.weight_list.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.weight_list.SetForegroundColour(wx.Colour(self.parent.text_dark))
        self.weight_list.SetTextColour(wx.Colour(self.parent.text_dark))
        self.weight_list.AppendColumn("Date", width=200)
        self.weight_list.AppendColumn("Weight (kg)", width=150)
        self.weight_list.AppendColumn("Notes", width=400)

        # Load all Dataset
        self.load_all_data()

        # Close button
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_btn = wx.Button(self, label="Close", size=(100, 35))
        close_btn.SetBackgroundColour(wx.Colour(self.parent.helen_color))
        close_btn.SetForegroundColour(wx.Colour(self.parent.button_text_color))
        close_btn.Bind(wx.EVT_BUTTON, lambda evt: self.Close())

        btn_sizer.Add(close_btn, 0, wx.ALIGN_CENTER)

        main_sizer.Add(self.weight_list, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        self.SetSizer(main_sizer)
        self.Centre()

    def load_all_data(self):
        """Load all weight history records"""
        self.weight_list.DeleteAllItems()

        if not self.user:
            return

        try:
            conn = sqlite3.connect('./Database/fitness_app.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT date, weight, notes FROM weight_history WHERE user_id = ? ORDER BY date DESC",
                (self.user['id'],)
            )
            records = cursor.fetchall()

            for i, (date, weight, notes) in enumerate(records):
                if isinstance(date, str):
                    date_str = date[:10]
                else:
                    date_str = str(date)

                index = self.weight_list.InsertItem(i, date_str)
                self.weight_list.SetItem(index, 1, f"{weight:.1f}")
                self.weight_list.SetItem(index, 2, notes if notes else "")

            conn.close()

        except sqlite3.Error as e:
            wx.MessageBox(f"Error loading Dataset: {e}", "Error", wx.OK | wx.ICON_ERROR)


class ExpandedWorkoutDialog(wx.Dialog):
    """Dialog for expanded workout history"""

    def __init__(self, parent, user):
        super(ExpandedWorkoutDialog, self).__init__(parent, title="Workout History - Full View", size=(1000, 600))
        self.user = user
        self.parent = parent

        self.SetBackgroundColour(parent.card_bg)
        self.InitUI()

    def InitUI(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create list control for all workout history
        self.workout_list = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.workout_list.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.workout_list.SetForegroundColour(wx.Colour(self.parent.text_dark))
        self.workout_list.SetTextColour(wx.Colour(self.parent.text_dark))
        self.workout_list.AppendColumn("Date", width=150)
        self.workout_list.AppendColumn("Type", width=120)
        self.workout_list.AppendColumn("Duration", width=100)
        self.workout_list.AppendColumn("Calories", width=100)
        self.workout_list.AppendColumn("Notes", width=450)

        # Load all Dataset
        self.load_all_data()

        # Close button
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_btn = wx.Button(self, label="Close", size=(100, 35))
        close_btn.SetBackgroundColour(wx.Colour(self.parent.helen_color))
        close_btn.SetForegroundColour(wx.Colour(self.parent.button_text_color))
        close_btn.Bind(wx.EVT_BUTTON, lambda evt: self.Close())

        btn_sizer.Add(close_btn, 0, wx.ALIGN_CENTER)

        main_sizer.Add(self.workout_list, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        self.SetSizer(main_sizer)
        self.Centre()

    def load_all_data(self):
        """Load all workout history records"""
        self.workout_list.DeleteAllItems()

        if not self.user:
            return

        try:
            conn = sqlite3.connect('./Database/fitness_app.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT date, workout_type, duration, calories_burned, notes FROM workout_history WHERE user_id = ? ORDER BY date DESC",
                (self.user['id'],)
            )
            records = cursor.fetchall()

            for i, (date, wtype, duration, calories, notes) in enumerate(records):
                if isinstance(date, str):
                    date_str = date[:10]
                else:
                    date_str = str(date)

                index = self.workout_list.InsertItem(i, date_str)
                self.workout_list.SetItem(index, 1, wtype)
                self.workout_list.SetItem(index, 2, str(duration))
                self.workout_list.SetItem(index, 3, str(calories))
                self.workout_list.SetItem(index, 4, notes if notes else "")

            conn.close()

        except sqlite3.Error as e:
            wx.MessageBox(f"Error loading Dataset: {e}", "Error", wx.OK | wx.ICON_ERROR)


class ExpandedDietDialog(wx.Dialog):
    """Dialog for expanded diet history"""

    def __init__(self, parent, user):
        super(ExpandedDietDialog, self).__init__(parent, title="Diet History - Full View", size=(1200, 600))
        self.user = user
        self.parent = parent

        self.SetBackgroundColour(parent.card_bg)
        self.InitUI()

    def InitUI(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create list control for all diet history
        self.diet_list = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.diet_list.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.diet_list.SetForegroundColour(wx.Colour(self.parent.text_dark))
        self.diet_list.SetTextColour(wx.Colour(self.parent.text_dark))
        self.diet_list.AppendColumn("Date", width=150)
        self.diet_list.AppendColumn("Meal", width=120)
        self.diet_list.AppendColumn("Calories", width=100)
        self.diet_list.AppendColumn("Protein", width=100)
        self.diet_list.AppendColumn("Carbs", width=100)
        self.diet_list.AppendColumn("Fats", width=100)
        self.diet_list.AppendColumn("Notes", width=400)

        # Load all Dataset
        self.load_all_data()

        # Close button
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_btn = wx.Button(self, label="Close", size=(100, 35))
        close_btn.SetBackgroundColour(wx.Colour(self.parent.helen_color))
        close_btn.SetForegroundColour(wx.Colour(self.parent.button_text_color))
        close_btn.Bind(wx.EVT_BUTTON, lambda evt: self.Close())

        btn_sizer.Add(close_btn, 0, wx.ALIGN_CENTER)

        main_sizer.Add(self.diet_list, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        self.SetSizer(main_sizer)
        self.Centre()

    def load_all_data(self):
        """Load all diet history records"""
        self.diet_list.DeleteAllItems()

        if not self.user:
            return

        try:
            conn = sqlite3.connect('./Database/fitness_app.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT date, meal_type, calories, protein, carbs, fats, notes FROM diet_history WHERE user_id = ? ORDER BY date DESC",
                (self.user['id'],)
            )
            records = cursor.fetchall()

            for i, (date, meal, cal, protein, carbs, fats, notes) in enumerate(records):
                if isinstance(date, str):
                    date_str = date[:10]
                else:
                    date_str = str(date)

                index = self.diet_list.InsertItem(i, date_str)
                self.diet_list.SetItem(index, 1, meal)
                self.diet_list.SetItem(index, 2, str(cal))
                self.diet_list.SetItem(index, 3, str(protein))
                self.diet_list.SetItem(index, 4, str(carbs))
                self.diet_list.SetItem(index, 5, str(fats))
                self.diet_list.SetItem(index, 6, notes if notes else "")

            conn.close()

        except sqlite3.Error as e:
            wx.MessageBox(f"Error loading Dataset: {e}", "Error", wx.OK | wx.ICON_ERROR)


class DetailViewDialog(wx.Dialog):
    """Dialog for viewing entry details"""

    def __init__(self, parent, title, details):
        super(DetailViewDialog, self).__init__(parent, title=title, size=(500, 400))
        self.parent = parent

        self.SetBackgroundColour(parent.card_bg)
        self.InitUI(details)

    def InitUI(self, details):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Text control for details
        text_ctrl = wx.TextCtrl(
            self,
            value=details,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2
        )
        text_ctrl.SetBackgroundColour(wx.Colour("#F8FAFC"))
        text_ctrl.SetForegroundColour(wx.Colour(self.parent.text_dark))
        text_ctrl.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # Close button
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_btn = wx.Button(self, label="Close", size=(100, 35))
        close_btn.SetBackgroundColour(wx.Colour(self.parent.helen_color))
        close_btn.SetForegroundColour(wx.Colour(self.parent.button_text_color))
        close_btn.Bind(wx.EVT_BUTTON, lambda evt: self.Close())

        btn_sizer.Add(close_btn, 0, wx.ALIGN_CENTER)

        main_sizer.Add(text_ctrl, 1, wx.EXPAND | wx.ALL, 15)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)

        self.SetSizer(main_sizer)
        self.Centre()


class EditProfileDialog(wx.Dialog):
    """Dialog for editing user profile"""

    def __init__(self, parent, title, user=None):
        super(EditProfileDialog, self).__init__(parent, title=title, size=(450, 450))

        self.user = user
        self.parent = parent

        # Color scheme
        self.primary_bg = "#EAF2FF"
        self.card_bg = "#FFFFFF"
        self.header_bg = "#2E5BFF"
        self.text_dark = "#000000"
        self.button_text_color = "#000000"

        self.SetBackgroundColour(self.card_bg)

        self.InitUI()
        self.load_profile_data()

    def InitUI(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(self, label="Edit Your Profile")
        title.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour(self.text_dark))

        # Form panel
        form_panel = wx.Panel(self)
        form_panel.SetBackgroundColour(self.primary_bg)
        form_sizer = wx.BoxSizer(wx.VERTICAL)

        label_font = wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # Age row
        age_sizer = wx.BoxSizer(wx.HORIZONTAL)
        age_label = wx.StaticText(form_panel, label="Age:")
        age_label.SetFont(label_font)
        age_label.SetForegroundColour(wx.Colour(self.text_dark))
        age_label.SetMinSize((100, -1))

        self.age_input = wx.TextCtrl(form_panel, size=(250, 35))
        self.age_input.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.age_input.SetForegroundColour(wx.Colour(self.text_dark))

        age_sizer.Add(age_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        age_sizer.Add(self.age_input, 1, wx.EXPAND)

        # Height row
        height_sizer = wx.BoxSizer(wx.HORIZONTAL)
        height_label = wx.StaticText(form_panel, label="Height (m):")
        height_label.SetFont(label_font)
        height_label.SetForegroundColour(wx.Colour(self.text_dark))
        height_label.SetMinSize((100, -1))

        self.height_input = wx.TextCtrl(form_panel, size=(250, 35))
        self.height_input.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.height_input.SetForegroundColour(wx.Colour(self.text_dark))

        height_sizer.Add(height_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        height_sizer.Add(self.height_input, 1, wx.EXPAND)

        # Weight row
        weight_sizer = wx.BoxSizer(wx.HORIZONTAL)
        weight_label = wx.StaticText(form_panel, label="Weight (kg):")
        weight_label.SetFont(label_font)
        weight_label.SetForegroundColour(wx.Colour(self.text_dark))
        weight_label.SetMinSize((100, -1))

        self.weight_input = wx.TextCtrl(form_panel, size=(250, 35))
        self.weight_input.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.weight_input.SetForegroundColour(wx.Colour(self.text_dark))

        weight_sizer.Add(weight_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        weight_sizer.Add(self.weight_input, 1, wx.EXPAND)

        # Gender row
        gender_sizer = wx.BoxSizer(wx.HORIZONTAL)
        gender_label = wx.StaticText(form_panel, label="Gender:")
        gender_label.SetFont(label_font)
        gender_label.SetForegroundColour(wx.Colour(self.text_dark))
        gender_label.SetMinSize((100, -1))

        self.gender_choice = wx.ComboBox(form_panel, choices=["Male", "Female"],
                                         style=wx.CB_READONLY, size=(250, 35))
        self.gender_choice.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.gender_choice.SetForegroundColour(wx.Colour(self.text_dark))
        self.gender_choice.SetSelection(0)

        gender_sizer.Add(gender_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        gender_sizer.Add(self.gender_choice, 1, wx.EXPAND)

        # Add all rows to form sizer
        form_sizer.Add(age_sizer, 0, wx.EXPAND | wx.ALL, 10)
        form_sizer.Add(height_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        form_sizer.Add(weight_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        form_sizer.Add(gender_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        form_panel.SetSizer(form_sizer)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        save_btn = wx.Button(self, label="Save Changes", size=(150, 40))
        save_btn.SetBackgroundColour(wx.Colour("#28A745"))
        save_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        save_btn.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)

        cancel_btn = wx.Button(self, label="Cancel", size=(150, 40))
        cancel_btn.SetBackgroundColour(wx.Colour("#DC3545"))
        cancel_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        cancel_btn.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        cancel_btn.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.ID_CANCEL))

        btn_sizer.Add(save_btn, 0, wx.RIGHT, 15)
        btn_sizer.Add(cancel_btn, 0)

        main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        main_sizer.Add(form_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 25)
        main_sizer.AddSpacer(30)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        self.SetSizer(main_sizer)

    def load_profile_data(self):
        if not self.user:
            return

        try:
            cursor = self.parent.cursor
            cursor.execute(
                "SELECT age, height, weight, gender FROM user_profiles WHERE user_id = ?",
                (self.user['id'],)
            )
            profile = cursor.fetchone()

            if profile:
                age, height, weight, gender = profile

                if age:
                    self.age_input.SetValue(str(age))
                if height:
                    self.height_input.SetValue(str(height))
                if weight:
                    self.weight_input.SetValue(str(weight))
                if gender:
                    self.gender_choice.SetValue(gender)

        except Exception as e:
            print(f"Error loading profile Dataset: {e}")

    def on_save(self, event):
        if not self.user:
            self.EndModal(wx.ID_CANCEL)
            return

        try:
            age = self.age_input.GetValue().strip()
            height = self.height_input.GetValue().strip()
            weight = self.weight_input.GetValue().strip()
            gender = self.gender_choice.GetValue()

            if age and not age.isdigit():
                wx.MessageBox("Please enter a valid age", "Error", wx.OK | wx.ICON_ERROR)
                return

            if height:
                try:
                    float(height)
                except ValueError:
                    wx.MessageBox("Please enter a valid height", "Error", wx.OK | wx.ICON_ERROR)
                    return

            if weight:
                try:
                    float(weight)
                except ValueError:
                    wx.MessageBox("Please enter a valid weight", "Error", wx.OK | wx.ICON_ERROR)
                    return

            age = int(age) if age else None
            height = float(height) if height else None
            weight = float(weight) if weight else None

            cursor = self.parent.cursor
            conn = self.parent.conn

            cursor.execute("SELECT id FROM user_profiles WHERE user_id = ?", (self.user['id'],))
            exists = cursor.fetchone()

            if exists:
                cursor.execute('''
                    UPDATE user_profiles 
                    SET age = ?, height = ?, weight = ?, gender = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (age, height, weight, gender, self.user['id']))
            else:
                cursor.execute('''
                    INSERT INTO user_profiles (user_id, age, height, weight, gender)
                    VALUES (?, ?, ?, ?, ?)
                ''', (self.user['id'], age, height, weight, gender))

            conn.commit()

            wx.MessageBox("Profile updated successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

        except Exception as e:
            wx.MessageBox(f"Error saving profile: {e}", "Error", wx.OK | wx.ICON_ERROR)


def main():
    app = wx.App(False)

    test_user = {
        'id': 1,
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com'
    }

    frame = ProfileApp(None, user=test_user)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()