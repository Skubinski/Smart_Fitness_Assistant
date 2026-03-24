import wx
import sqlite3
import hashlib
from datetime import datetime


class LoginApp(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(LoginApp, self).__init__(*args, **kwargs)

        # Color scheme
        self.primary_bg = "#EAF2FF"  # Light Blue
        self.card_bg = "#FFFFFF"  # White
        self.header_bg = "#2E5BFF"  # Blue header
        self.helen_color = "#4A90E2"  # Blue Buttons
        self.helen_hover = "#357ABD"  # Darker Blue Hover
        self.accent_green = "#28A745"  # Green Buttons
        self.green_hover = "#1E7E34"  # Darker Green Hover
        self.text_dark = "#000000"  # Black Text
        self.text_muted = "#333333"  # Dark Gray for muted text
        self.border = "#CCCCCC"  # Light Gray for Borders

        # Button text colors
        self.button_text_color = "#000000"

        # Dataset connection
        self.conn = None
        self.cursor = None
        self.init_database()

        self.InitUI()

    def init_database(self):
        """Initialize database connection and create users table if not exists"""
        try:
            self.conn = sqlite3.connect('./Database/fitness_app.db')
            self.cursor = self.conn.cursor()

            # Users table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            wx.MessageBox(f"Error initializing database: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def InitUI(self):
        self.SetTitle("Smart Fitness Assistant - Login & Registration")
        self.SetSize((1000, 700))
        self.SetMinSize((900, 600))
        self.SetBackgroundColour(self.primary_bg)

        # Main panel
        panel = wx.Panel(self)
        panel.SetBackgroundColour(self.primary_bg)

        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # ===== Header =====
        header_panel = wx.Panel(panel)
        header_panel.SetBackgroundColour(self.header_bg)
        header_sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(header_panel, label="Smart Fitness Assistant")
        title.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour("WHITE"))

        subtitle = wx.StaticText(
            header_panel,
            label="Your personal assistant for fitness and nutrition"
        )
        subtitle.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        subtitle.SetForegroundColour(wx.Colour(230, 235, 255))

        header_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 15)
        header_sizer.Add(subtitle, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER, 15)
        header_panel.SetSizer(header_sizer)

        main_sizer.Add(header_panel, 0, wx.EXPAND | wx.ALL, 10)

        # ===== Main Content =====
        content_panel = wx.Panel(panel)
        content_panel.SetBackgroundColour(self.primary_bg)
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left part - App Information
        left_panel = wx.Panel(content_panel)
        left_panel.SetBackgroundColour(self.card_bg)
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Icon/Logo
        logo_text = wx.StaticText(left_panel, label="🏋️‍♂️")
        logo_text.SetFont(wx.Font(84, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        logo_text.SetForegroundColour(wx.Colour(self.header_bg))

        welcome_title = wx.StaticText(left_panel, label="Welcome!")
        welcome_title.SetFont(wx.Font(28, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        welcome_title.SetForegroundColour(wx.Colour(self.text_dark))

        welcome_text = wx.StaticText(
            left_panel,
            label="Smart Fitness Assistant helps you achieve your fitness goals with personalized diet and exercise plans."
        )
        welcome_text.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        welcome_text.SetForegroundColour(wx.Colour(self.text_muted))
        welcome_text.Wrap(400)

        # Features list
        features = wx.Panel(left_panel)
        features.SetBackgroundColour(self.card_bg)
        features_sizer = wx.BoxSizer(wx.VERTICAL)

        feature_font = wx.Font(13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        feature1 = wx.StaticText(features, label="✓ Personalized diet plans")
        feature1.SetFont(feature_font)
        feature1.SetForegroundColour(wx.Colour(self.text_dark))

        feature2 = wx.StaticText(features, label="✓ Training programs based on your goals")
        feature2.SetFont(feature_font)
        feature2.SetForegroundColour(wx.Colour(self.text_dark))

        feature3 = wx.StaticText(features, label="✓ Progress tracking")
        feature3.SetFont(feature_font)
        feature3.SetForegroundColour(wx.Colour(self.text_dark))

        feature4 = wx.StaticText(features, label="✓ We believe in you!")
        feature4.SetFont(feature_font)
        feature4.SetForegroundColour(wx.Colour(self.text_dark))

        features_sizer.Add(feature1, 0, wx.BOTTOM, 10)
        features_sizer.Add(feature2, 0, wx.BOTTOM, 10)
        features_sizer.Add(feature3, 0, wx.BOTTOM, 10)
        features_sizer.Add(feature4, 0, wx.BOTTOM, 10)
        features.SetSizer(features_sizer)

        left_sizer.Add(logo_text, 0, wx.ALL | wx.ALIGN_CENTER, 30)
        left_sizer.Add(welcome_title, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER, 15)
        left_sizer.Add(welcome_text, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER, 30)
        left_sizer.Add(features, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER, 20)

        left_panel.SetSizer(left_sizer)

        # Right part - Login/Registration Form
        right_panel = wx.Panel(content_panel)
        right_panel.SetBackgroundColour(self.card_bg)
        right_sizer = wx.BoxSizer(wx.VERTICAL)


        # Tabs and Buttons Panel
        tab_button_panel = wx.Panel(right_panel)
        tab_button_panel.SetBackgroundColour(self.card_bg)
        tab_button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Creating Tabs and Buttons
        self.login_tab_btn = wx.Button(tab_button_panel, label="🔐 Login", size=(150, 45))
        self.login_tab_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        self.login_tab_btn.SetForegroundColour(wx.Colour(self.text_dark))  # ЧЕРЕН ТЕКСТ
        self.login_tab_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.login_tab_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.login_tab_btn.Bind(wx.EVT_BUTTON, self.on_login_tab_click)
        self.login_tab_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.login_tab_btn, self.helen_hover)
        )
        self.login_tab_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.login_tab_btn, self.helen_color)
        )

        self.register_tab_btn = wx.Button(tab_button_panel, label="📝 Register", size=(150, 45))
        self.register_tab_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        self.register_tab_btn.SetForegroundColour(wx.Colour(self.text_dark))  # ЧЕРЕН ТЕКСТ
        self.register_tab_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.register_tab_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.register_tab_btn.Bind(wx.EVT_BUTTON, self.on_register_tab_click)
        self.register_tab_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.register_tab_btn, self.helen_hover)
        )
        self.register_tab_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.register_tab_btn, self.helen_color)
        )

        # Adding Buttons in the Center
        tab_button_sizer.AddStretchSpacer(1)
        tab_button_sizer.Add(self.login_tab_btn, 0, wx.RIGHT, 15)
        tab_button_sizer.Add(self.register_tab_btn, 0)
        tab_button_sizer.AddStretchSpacer(1)

        tab_button_panel.SetSizer(tab_button_sizer)

        # Simplebook
        self.book = wx.Simplebook(right_panel)
        self.book.SetBackgroundColour(self.card_bg)

        # Login panel
        self.login_panel = wx.Panel(self.book)
        self.login_panel.SetBackgroundColour(self.card_bg)
        self.create_login_ui()

        # Registration panel
        self.register_panel = wx.Panel(self.book)
        self.register_panel.SetBackgroundColour(self.card_bg)
        self.create_register_ui()

        self.book.AddPage(self.login_panel, "Login")
        self.book.AddPage(self.register_panel, "Register")

        self.book.SetSelection(0)
        self.login_tab_btn.SetBackgroundColour(wx.Colour(self.accent_green))

        right_sizer.Add(tab_button_panel, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 20)
        right_sizer.Add(self.book, 1, wx.EXPAND | wx.ALL, 10)

        right_panel.SetSizer(right_sizer)

        # Add left and right panels to content_sizer
        content_sizer.Add(left_panel, 1, wx.EXPAND | wx.RIGHT, 10)
        content_sizer.Add(right_panel, 1, wx.EXPAND | wx.LEFT, 10)

        content_panel.SetSizer(content_sizer)
        main_sizer.Add(content_panel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # Footer
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

    def create_login_ui(self):
        """Create the login form UI"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Form title
        form_title = wx.StaticText(self.login_panel, label="Login to Your Account")
        form_title.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        form_title.SetForegroundColour(wx.Colour(self.text_dark))

        # Form panel
        form_panel = wx.Panel(self.login_panel)
        form_panel.SetBackgroundColour(self.primary_bg)
        form_sizer = wx.BoxSizer(wx.VERTICAL)

        label_font = wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # Username
        username_sizer = wx.BoxSizer(wx.HORIZONTAL)
        username_label = wx.StaticText(form_panel, label="Username:")
        username_label.SetFont(label_font)
        username_label.SetForegroundColour(wx.Colour(self.text_dark))
        username_label.SetMinSize((100, -1))

        self.login_username = wx.TextCtrl(form_panel, size=(250, 35))
        self.login_username.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.login_username.SetForegroundColour(wx.Colour(self.text_dark))

        username_sizer.Add(username_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        username_sizer.Add(self.login_username, 1, wx.EXPAND)

        # Password
        password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        password_label = wx.StaticText(form_panel, label="Password:")
        password_label.SetFont(label_font)
        password_label.SetForegroundColour(wx.Colour(self.text_dark))
        password_label.SetMinSize((100, -1))

        self.login_password = wx.TextCtrl(form_panel, size=(250, 35), style=wx.TE_PASSWORD)
        self.login_password.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.login_password.SetForegroundColour(wx.Colour(self.text_dark))

        password_sizer.Add(password_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        password_sizer.Add(self.login_password, 1, wx.EXPAND)

        form_sizer.Add(username_sizer, 0, wx.EXPAND | wx.ALL, 10)
        form_sizer.Add(password_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        form_panel.SetSizer(form_sizer)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.login_btn = wx.Button(self.login_panel, label="Login", size=(150, 45))
        self.login_btn.SetBackgroundColour(wx.Colour(self.accent_green))
        self.login_btn.SetForegroundColour(wx.Colour(self.text_dark))
        self.login_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.login_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.login_btn.Bind(wx.EVT_BUTTON, self.on_login)
        self.login_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.login_btn, self.green_hover)
        )
        self.login_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.login_btn, self.accent_green)
        )

        self.clear_btn = wx.Button(self.login_panel, label="Clear", size=(150, 45))
        self.clear_btn.SetBackgroundColour(wx.Colour("#6C757D"))
        self.clear_btn.SetForegroundColour(wx.Colour(self.text_dark))
        self.clear_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.clear_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.clear_btn.Bind(wx.EVT_BUTTON, self.on_login_clear)
        self.clear_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.clear_btn, "#5A6268")
        )
        self.clear_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.clear_btn, "#6C757D")
        )

        btn_sizer.Add(self.login_btn, 0, wx.RIGHT, 15)
        btn_sizer.Add(self.clear_btn, 0)

        main_sizer.Add(form_title, 0, wx.ALL | wx.ALIGN_CENTER, 30)
        main_sizer.Add(form_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        main_sizer.AddSpacer(30)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 30)

        self.login_panel.SetSizer(main_sizer)

    def create_register_ui(self):
        """Create the registration form UI"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Form title
        form_title = wx.StaticText(self.register_panel, label="Create New Account")
        form_title.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        form_title.SetForegroundColour(wx.Colour(self.text_dark))

        # Form panel
        form_panel = wx.Panel(self.register_panel)
        form_panel.SetBackgroundColour(self.primary_bg)
        form_sizer = wx.BoxSizer(wx.VERTICAL)

        label_font = wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # Username
        username_sizer = wx.BoxSizer(wx.HORIZONTAL)
        username_label = wx.StaticText(form_panel, label="Username:*")
        username_label.SetFont(label_font)
        username_label.SetForegroundColour(wx.Colour(self.text_dark))
        username_label.SetMinSize((120, -1))

        self.reg_username = wx.TextCtrl(form_panel, size=(250, 35))
        self.reg_username.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.reg_username.SetForegroundColour(wx.Colour(self.text_dark))

        username_sizer.Add(username_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        username_sizer.Add(self.reg_username, 1, wx.EXPAND)

        # Email
        email_sizer = wx.BoxSizer(wx.HORIZONTAL)
        email_label = wx.StaticText(form_panel, label="Email:*")
        email_label.SetFont(label_font)
        email_label.SetForegroundColour(wx.Colour(self.text_dark))
        email_label.SetMinSize((120, -1))

        self.reg_email = wx.TextCtrl(form_panel, size=(250, 35))
        self.reg_email.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.reg_email.SetForegroundColour(wx.Colour(self.text_dark))

        email_sizer.Add(email_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        email_sizer.Add(self.reg_email, 1, wx.EXPAND)

        # First Name
        firstname_sizer = wx.BoxSizer(wx.HORIZONTAL)
        firstname_label = wx.StaticText(form_panel, label="First Name:")
        firstname_label.SetFont(label_font)
        firstname_label.SetForegroundColour(wx.Colour(self.text_dark))
        firstname_label.SetMinSize((120, -1))

        self.reg_firstname = wx.TextCtrl(form_panel, size=(250, 35))
        self.reg_firstname.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.reg_firstname.SetForegroundColour(wx.Colour(self.text_dark))

        firstname_sizer.Add(firstname_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        firstname_sizer.Add(self.reg_firstname, 1, wx.EXPAND)

        # Last Name
        lastname_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lastname_label = wx.StaticText(form_panel, label="Last Name:")
        lastname_label.SetFont(label_font)
        lastname_label.SetForegroundColour(wx.Colour(self.text_dark))
        lastname_label.SetMinSize((120, -1))

        self.reg_lastname = wx.TextCtrl(form_panel, size=(250, 35))
        self.reg_lastname.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.reg_lastname.SetForegroundColour(wx.Colour(self.text_dark))

        lastname_sizer.Add(lastname_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        lastname_sizer.Add(self.reg_lastname, 1, wx.EXPAND)

        # Password
        password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        password_label = wx.StaticText(form_panel, label="Password:*")
        password_label.SetFont(label_font)
        password_label.SetForegroundColour(wx.Colour(self.text_dark))
        password_label.SetMinSize((120, -1))

        self.reg_password = wx.TextCtrl(form_panel, size=(250, 35), style=wx.TE_PASSWORD)
        self.reg_password.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.reg_password.SetForegroundColour(wx.Colour(self.text_dark))

        password_sizer.Add(password_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        password_sizer.Add(self.reg_password, 1, wx.EXPAND)

        # Confirm Password
        confirm_sizer = wx.BoxSizer(wx.HORIZONTAL)
        confirm_label = wx.StaticText(form_panel, label="Confirm Password:*")
        confirm_label.SetFont(label_font)
        confirm_label.SetForegroundColour(wx.Colour(self.text_dark))
        confirm_label.SetMinSize((120, -1))

        self.reg_confirm = wx.TextCtrl(form_panel, size=(250, 35), style=wx.TE_PASSWORD)
        self.reg_confirm.SetBackgroundColour(wx.Colour("#FFFFFF"))
        self.reg_confirm.SetForegroundColour(wx.Colour(self.text_dark))

        confirm_sizer.Add(confirm_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        confirm_sizer.Add(self.reg_confirm, 1, wx.EXPAND)

        # Add all to form_sizer
        form_sizer.Add(username_sizer, 0, wx.EXPAND | wx.ALL, 10)
        form_sizer.Add(email_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        form_sizer.Add(firstname_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        form_sizer.Add(lastname_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        form_sizer.Add(password_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        form_sizer.Add(confirm_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        form_panel.SetSizer(form_sizer)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.register_btn = wx.Button(self.register_panel, label="Register", size=(150, 45))
        self.register_btn.SetBackgroundColour(wx.Colour(self.accent_green))
        self.register_btn.SetForegroundColour(wx.Colour(self.text_dark))
        self.register_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.register_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.register_btn.Bind(wx.EVT_BUTTON, self.on_register)
        self.register_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.register_btn, self.green_hover)
        )
        self.register_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.register_btn, self.accent_green)
        )

        self.clear_reg_btn = wx.Button(self.register_panel, label="Clear", size=(150, 45))
        self.clear_reg_btn.SetBackgroundColour(wx.Colour("#6C757D"))
        self.clear_reg_btn.SetForegroundColour(wx.Colour(self.text_dark))
        self.clear_reg_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.clear_reg_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.clear_reg_btn.Bind(wx.EVT_BUTTON, self.on_register_clear)
        self.clear_reg_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.clear_reg_btn, "#5A6268")
        )
        self.clear_reg_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.clear_reg_btn, "#6C757D")
        )

        btn_sizer.Add(self.register_btn, 0, wx.RIGHT, 15)
        btn_sizer.Add(self.clear_reg_btn, 0)

        # Required fields note
        note_text = wx.StaticText(self.register_panel, label="* Required fields")
        note_text.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        note_text.SetForegroundColour(wx.Colour(self.text_muted))

        main_sizer.Add(form_title, 0, wx.ALL | wx.ALIGN_CENTER, 30)
        main_sizer.Add(form_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        main_sizer.Add(note_text, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 20)

        self.register_panel.SetSizer(main_sizer)

    def on_login_tab_click(self, event=None):
        """Switch to login tab"""
        self.book.SetSelection(0)
        # Visual feedback for active tab
        self.login_tab_btn.SetBackgroundColour(wx.Colour(self.accent_green))
        self.register_tab_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        if event:
            event.Skip()

    def on_register_tab_click(self, event=None):
        """Switch to register tab"""
        self.book.SetSelection(1)
        # Visual feedback for active tab
        self.register_tab_btn.SetBackgroundColour(wx.Colour(self.accent_green))
        self.login_tab_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        if event:
            event.Skip()

    def on_register(self, event):
        """Handle register button click"""
        # Get form values
        username = self.reg_username.GetValue().strip()
        email = self.reg_email.GetValue().strip()
        first_name = self.reg_firstname.GetValue().strip()
        last_name = self.reg_lastname.GetValue().strip()
        password = self.reg_password.GetValue()
        confirm = self.reg_confirm.GetValue()

        # Validation
        if not username or not email or not password or not confirm:
            wx.MessageBox("Please fill in all required fields", "Error", wx.OK | wx.ICON_ERROR)
            return

        if password != confirm:
            wx.MessageBox("Passwords do not match", "Error", wx.OK | wx.ICON_ERROR)
            return

        if len(password) < 6:
            wx.MessageBox("Password must be at least 6 characters long", "Error", wx.OK | wx.ICON_ERROR)
            return

        if "@" not in email or "." not in email:
            wx.MessageBox("Please enter a valid email address", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            # Check if username exists
            self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if self.cursor.fetchone():
                wx.MessageBox("Username already exists", "Error", wx.OK | wx.ICON_ERROR)
                return

            # Check if email exists
            self.cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if self.cursor.fetchone():
                wx.MessageBox("Email already registered", "Error", wx.OK | wx.ICON_ERROR)
                return

            # Insert new user
            hashed_password = self.hash_password(password)
            self.cursor.execute('''
                INSERT INTO users (username, password, email, first_name, last_name, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, email, first_name, last_name, datetime.now()))

            self.conn.commit()

            wx.MessageBox("Registration successful! You can now login.", "Success",
                          wx.OK | wx.ICON_INFORMATION)

            # Clear form and switch to login tab
            self.on_register_clear(None)
            self.on_login_tab_click()

        except sqlite3.Error as e:
            wx.MessageBox(f"Database error: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_button_hover(self, event, button, color):
        button.SetBackgroundColour(wx.Colour(color))
        button.Refresh()
        event.Skip()

    def on_button_leave(self, event, button, color):
        button.SetBackgroundColour(wx.Colour(color))
        button.Refresh()
        event.Skip()

    def on_login_clear(self, event):
        """Clear login form"""
        self.login_username.SetValue("")
        self.login_password.SetValue("")

    def on_register_clear(self, event):
        """Clear registration form"""
        self.reg_username.SetValue("")
        self.reg_email.SetValue("")
        self.reg_firstname.SetValue("")
        self.reg_lastname.SetValue("")
        self.reg_password.SetValue("")
        self.reg_confirm.SetValue("")

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def on_login(self, event):
        """Handle login button click"""
        username = self.login_username.GetValue().strip()
        password = self.login_password.GetValue()

        if not username or not password:
            wx.MessageBox("Please enter username and password", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            hashed_password = self.hash_password(password)
            self.cursor.execute(
                "SELECT id, username, email, first_name, last_name FROM users WHERE username = ? AND password = ?",
                (username, hashed_password)
            )
            user = self.cursor.fetchone()

            if user:
                user_dict = {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'first_name': user[3],
                    'last_name': user[4]
                }

                wx.MessageBox(f"Welcome back, {user_dict['first_name'] or user_dict['username']}!",
                            "Login Successful", wx.OK | wx.ICON_INFORMATION)

                # Open main app
                try:
                    from UI.program_GUI import FitnessApp
                    main_app = FitnessApp(None, user=user_dict)
                    main_app.Show()
                    self.Close()
                except ImportError as e:
                    wx.MessageBox(f"Could not open main application: {e}", "Error", wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox("Invalid username or password", "Login Failed", wx.OK | wx.ICON_ERROR)

        except sqlite3.Error as e:
            wx.MessageBox(f"Database error: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_register(self, event):
        """Handle register button click"""
        # Get form values
        username = self.reg_username.GetValue().strip()
        email = self.reg_email.GetValue().strip()
        first_name = self.reg_firstname.GetValue().strip()
        last_name = self.reg_lastname.GetValue().strip()
        password = self.reg_password.GetValue()
        confirm = self.reg_confirm.GetValue()

        # Validation
        if not username or not email or not password or not confirm:
            wx.MessageBox("Please fill in all required fields", "Error", wx.OK | wx.ICON_ERROR)
            return

        if password != confirm:
            wx.MessageBox("Passwords do not match", "Error", wx.OK | wx.ICON_ERROR)
            return

        if len(password) < 6:
            wx.MessageBox("Password must be at least 6 characters long", "Error", wx.OK | wx.ICON_ERROR)
            return

        if "@" not in email or "." not in email:
            wx.MessageBox("Please enter a valid email address", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            # Check if username exists
            self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if self.cursor.fetchone():
                wx.MessageBox("Username already exists", "Error", wx.OK | wx.ICON_ERROR)
                return

            # Check if email exists
            self.cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if self.cursor.fetchone():
                wx.MessageBox("Email already registered", "Error", wx.OK | wx.ICON_ERROR)
                return

            # Insert new user
            hashed_password = self.hash_password(password)
            self.cursor.execute('''
                INSERT INTO users (username, password, email, first_name, last_name, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, email, first_name, last_name, datetime.now()))

            self.conn.commit()

            wx.MessageBox("Registration successful! You can now login.", "Success",
                        wx.OK | wx.ICON_INFORMATION)

            # Clear form and switch to login tab
            self.on_register_clear(None)
            self.on_login_tab_click(None)

        except sqlite3.Error as e:
            wx.MessageBox(f"Database error: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()


def main():
    app = wx.App(False)
    frame = LoginApp(None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()