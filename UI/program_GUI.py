import wx
import pandas as pd
import joblib
import sqlite3


class FitnessApp(wx.Frame):
    def __init__(self, *args, user=None, **kwargs):
        super(FitnessApp, self).__init__(*args, **kwargs)

        self.model_diet = joblib.load("./Models/diet_model_rfc.pkl")
        self.model_exercises = joblib.load("./Models/exercise_model_rfc.pkl")

        self.primary_bg = "#EAF2FF"
        self.card_bg = "#FFFFFF"
        self.header_bg = "#2E5BFF"
        self.helen_color = "#4A90E2"
        self.text_dark = "#1F2937"
        self.text_muted = "#6B7280"
        self.border = "#D6DCE5"
        self.button_hover = "#1E40AF"
        self.helen_hover = "#357ABD"

        # Green colors for diet button
        self.diet_btn_color = "#28A745"
        self.diet_btn_hover = "#1E7E34"

        # Button text color
        self.button_text_color = "#000000"

        self.input_bg = "#FFFFFF"
        self.input_fg = "#000000"

        # User Dataset - using Dataset from login_GUI
        self.current_user = user

        self.InitUI()

    def InitUI(self):
        self.SetTitle("Smart Fitness Assistant")
        self.SetSize((1180, 820))
        self.SetMinSize((1080, 760))
        self.SetBackgroundColour(self.primary_bg)

        panel = wx.Panel(self)
        panel.SetBackgroundColour(self.primary_bg)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # HEADER
        header_panel = wx.Panel(panel)
        header_panel.SetBackgroundColour(self.header_bg)
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Title and user info
        title_sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(header_panel, label="Smart Fitness Assistant")
        title.SetFont(wx.Font(22, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour("WHITE"))

        if self.current_user:
            welcome_text = f"Welcome, {self.current_user.get('first_name') or self.current_user.get('username')}!"
        else:
            welcome_text = "Get a personalized diet and exercise plan based on your body and health details."

        subtitle = wx.StaticText(
            header_panel,
            label=welcome_text
        )
        subtitle.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        subtitle.SetForegroundColour(wx.Colour(230, 235, 255))

        title_sizer.Add(title, 0, wx.ALL, 12)
        title_sizer.Add(subtitle, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

        # Profile and Logout buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.profile_btn = wx.Button(header_panel, label="👤 Profile")
        self.profile_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        self.profile_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        self.profile_btn.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.profile_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.profile_btn.Bind(wx.EVT_BUTTON, self.on_profile)
        self.profile_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.profile_btn, self.helen_hover)
        )
        self.profile_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.profile_btn, self.helen_color)
        )

        self.logout_btn = wx.Button(header_panel, label="🚪 Logout")
        self.logout_btn.SetBackgroundColour(wx.Colour("#DC3545"))
        self.logout_btn.SetForegroundColour(wx.Colour(self.button_text_color))
        self.logout_btn.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
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

        btn_sizer.Add(self.profile_btn, 0, wx.RIGHT, 10)
        btn_sizer.Add(self.logout_btn, 0)

        header_sizer.Add(title_sizer, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        header_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)

        header_panel.SetSizer(header_sizer)
        main_sizer.Add(header_panel, 0, wx.EXPAND | wx.ALL, 10)

        # CONTENT AREA
        content_panel = wx.Panel(panel)
        content_panel.SetBackgroundColour(self.primary_bg)
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # LEFT CARD
        left_card = wx.Panel(content_panel)
        left_card.SetBackgroundColour(self.card_bg)
        left_card.SetMinSize((480, -1))
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        left_title = wx.StaticText(left_card, label="Enter Your Fitness Details")
        left_title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        left_title.SetForegroundColour(wx.Colour(self.text_dark))

        left_desc = wx.StaticText(
            left_card,
            label="Fill in your body and health information to calculate your stats and generate a fitness plan."
        )
        left_desc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        left_desc.SetForegroundColour(wx.Colour(self.text_muted))
        left_desc.Wrap(400)

        # Form grid
        form_grid = wx.FlexGridSizer(rows=0, cols=2, vgap=14, hgap=12)
        form_grid.AddGrowableCol(1, 1)

        label_font = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        def make_label(parent, text):
            lbl = wx.StaticText(parent, label=text)
            lbl.SetFont(label_font)
            lbl.SetForegroundColour(wx.Colour(self.text_dark))
            return lbl

        def style_textctrl(ctrl):
            ctrl.SetMinSize((220, 35))
            ctrl.SetBackgroundColour(wx.Colour(self.input_bg))
            ctrl.SetForegroundColour(wx.Colour(self.input_fg))
            return ctrl

        def style_combobox(ctrl):
            ctrl.SetMinSize((220, 35))
            ctrl.SetBackgroundColour(wx.Colour(self.input_bg))
            ctrl.SetForegroundColour(wx.Colour(self.input_fg))
            if hasattr(ctrl, 'GetTextCtrl'):
                text_ctrl = ctrl.GetTextCtrl()
                if text_ctrl:
                    text_ctrl.SetBackgroundColour(wx.Colour(self.input_bg))
                    text_ctrl.SetForegroundColour(wx.Colour(self.input_fg))
            return ctrl

        # Input fields
        self.sex_choice = wx.ComboBox(left_card, choices=["Male", "Female"], style=wx.CB_READONLY)
        self.sex_choice.SetSelection(0)
        self.sex_choice = style_combobox(self.sex_choice)

        self.age_input = wx.TextCtrl(left_card)
        self.age_input = style_textctrl(self.age_input)

        self.height_input = wx.TextCtrl(left_card)
        self.height_input = style_textctrl(self.height_input)

        self.weight_input = wx.TextCtrl(left_card)
        self.weight_input = style_textctrl(self.weight_input)

        # Hypertension radio with Yes/No labels
        hp_panel = wx.Panel(left_card)
        hp_panel.SetBackgroundColour(self.card_bg)
        hp_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create radio buttons with explicit labels
        self.radio_hp_yes = wx.RadioButton(hp_panel, label="Yes", style=wx.RB_GROUP)
        self.radio_hp_no = wx.RadioButton(hp_panel, label="No")
        self.radio_hp_no.SetValue(True)

        hp_sizer.Add(self.radio_hp_yes, 0, wx.RIGHT, 20)
        hp_sizer.Add(self.radio_hp_no, 0)
        hp_panel.SetSizer(hp_sizer)

        # Diabetes radio with Yes/No labels
        diabetes_panel = wx.Panel(left_card)
        diabetes_panel.SetBackgroundColour(self.card_bg)
        diabetes_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create radio buttons with explicit labels
        self.radio_d_yes = wx.RadioButton(diabetes_panel, label="Yes", style=wx.RB_GROUP)
        self.radio_d_no = wx.RadioButton(diabetes_panel, label="No")
        self.radio_d_no.SetValue(True)

        diabetes_sizer.Add(self.radio_d_yes, 0, wx.RIGHT, 20)
        diabetes_sizer.Add(self.radio_d_no, 0)
        diabetes_panel.SetSizer(diabetes_sizer)

        # Goal combo
        self.goal_choice = wx.ComboBox(left_card, choices=["Weight Gain", "Weight Loss"], style=wx.CB_READONLY)
        self.goal_choice.SetSelection(0)
        self.goal_choice = style_combobox(self.goal_choice)

        # Add to form grid
        form_grid.Add(make_label(left_card, "Gender"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_grid.Add(self.sex_choice, 1, wx.EXPAND)

        form_grid.Add(make_label(left_card, "Age"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_grid.Add(self.age_input, 1, wx.EXPAND)

        form_grid.Add(make_label(left_card, "Height (m)"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_grid.Add(self.height_input, 1, wx.EXPAND)

        form_grid.Add(make_label(left_card, "Weight (kg)"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_grid.Add(self.weight_input, 1, wx.EXPAND)

        form_grid.Add(make_label(left_card, "Hypertension"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_grid.Add(hp_panel, 1, wx.EXPAND)

        form_grid.Add(make_label(left_card, "Diabetes"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_grid.Add(diabetes_panel, 1, wx.EXPAND)

        form_grid.Add(make_label(left_card, "Fitness Goal"), 0, wx.ALIGN_CENTER_VERTICAL)
        form_grid.Add(self.goal_choice, 1, wx.EXPAND)

        # BUTTONS
        self.calculate_btn = wx.Button(left_card, label="Calculate Health Stats")
        self.calculate_btn.SetMinSize((420, 50))
        self.calculate_btn.SetMaxSize((420, 50))
        self.calculate_btn.SetBackgroundColour(wx.Colour(self.helen_color))
        self.calculate_btn.SetForegroundColour(wx.Colour("BLACK"))
        self.calculate_btn.SetFont(wx.Font(13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.calculate_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.calculate_btn.Bind(wx.EVT_BUTTON, self.OnCalculate)
        self.calculate_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.calculate_btn, self.helen_hover)
        )
        self.calculate_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.calculate_btn, self.helen_color)
        )

        self.diet_btn = wx.Button(left_card, label="Generate Fitness Plan")
        self.diet_btn.SetMinSize((420, 50))
        self.diet_btn.SetMaxSize((420, 50))
        self.diet_btn.SetBackgroundColour(wx.Colour(self.diet_btn_color))
        self.diet_btn.SetForegroundColour(wx.Colour("BLACK"))
        self.diet_btn.SetFont(wx.Font(13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.diet_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.diet_btn.Bind(wx.EVT_BUTTON, self.OnDiet)
        self.diet_btn.Bind(
            wx.EVT_ENTER_WINDOW,
            lambda evt: self.on_button_hover(evt, self.diet_btn, self.diet_btn_hover)
        )
        self.diet_btn.Bind(
            wx.EVT_LEAVE_WINDOW,
            lambda evt: self.on_button_leave(evt, self.diet_btn, self.diet_btn_color)
        )
        self.diet_btn.Hide()

        # ADD TO LEFT SIZER
        left_sizer.Add(left_title, 0, wx.ALL, 15)
        left_sizer.Add(left_desc, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        left_sizer.Add(form_grid, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        left_sizer.AddSpacer(30)
        left_sizer.Add(self.calculate_btn, 0, wx.CENTER | wx.BOTTOM, 12)
        left_sizer.Add(self.diet_btn, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 18)

        left_card.SetSizer(left_sizer)

        # RIGHT SIDE
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        # Stats Card
        stats_card = wx.Panel(content_panel)
        stats_card.SetBackgroundColour(self.card_bg)
        stats_sizer = wx.BoxSizer(wx.VERTICAL)

        stats_title = wx.StaticText(stats_card, label="Health Statistics")
        stats_title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        stats_title.SetForegroundColour(wx.Colour(self.text_dark))

        self.stats_grid = wx.FlexGridSizer(rows=0, cols=2, vgap=12, hgap=25)
        self.stats_grid.AddGrowableCol(1, 1)

        self.bmi_score = wx.StaticText(stats_card, label="-")
        self.level_score = wx.StaticText(stats_card, label="-")
        self.bmr_score = wx.StaticText(stats_card, label="-")
        self.tdee_score = wx.StaticText(stats_card, label="-")
        self.target_calories_score = wx.StaticText(stats_card, label="-")
        self.act_factor_score = wx.StaticText(stats_card, label="-")

        value_font = wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        for ctrl in [
            self.bmi_score, self.level_score, self.bmr_score,
            self.tdee_score, self.target_calories_score, self.act_factor_score
        ]:
            ctrl.SetFont(value_font)
            ctrl.SetForegroundColour(wx.Colour(self.helen_color))

        def add_stat_row(label, value_ctrl):
            lbl = wx.StaticText(stats_card, label=label)
            lbl.SetFont(label_font)
            lbl.SetForegroundColour(wx.Colour(self.text_dark))
            self.stats_grid.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
            self.stats_grid.Add(value_ctrl, 0, wx.ALIGN_LEFT)

        add_stat_row("BMI", self.bmi_score)
        add_stat_row("Weight Level", self.level_score)
        add_stat_row("BMR", self.bmr_score)
        add_stat_row("TDEE", self.tdee_score)
        add_stat_row("Target Calories", self.target_calories_score)
        add_stat_row("Activity Factor", self.act_factor_score)

        stats_sizer.Add(stats_title, 0, wx.ALL, 15)
        stats_sizer.Add(self.stats_grid, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        stats_card.SetSizer(stats_sizer)

        # Result Card
        result_card = wx.Panel(content_panel)
        result_card.SetBackgroundColour(self.card_bg)
        result_sizer = wx.BoxSizer(wx.VERTICAL)

        result_title = wx.StaticText(result_card, label="Your Personalized Plan")
        result_title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        result_title.SetForegroundColour(wx.Colour(self.text_dark))

        self.result_text = wx.TextCtrl(
            result_card,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.BORDER_NONE
        )
        self.result_text.SetBackgroundColour(wx.Colour("#F8FAFC"))
        self.result_text.SetForegroundColour(wx.Colour(self.text_dark))
        self.result_text.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.result_text.SetMinSize((450, 350))
        self.result_text.SetValue(
            "Your diet and exercise recommendations will appear here after calculation."
        )

        result_sizer.Add(result_title, 0, wx.ALL, 15)
        result_sizer.Add(self.result_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        result_card.SetSizer(result_sizer)

        right_sizer.Add(stats_card, 0, wx.EXPAND | wx.BOTTOM, 10)
        right_sizer.Add(result_card, 1, wx.EXPAND)

        content_sizer.Add(left_card, 0, wx.EXPAND | wx.RIGHT, 15)
        content_sizer.Add(right_sizer, 1, wx.EXPAND)

        content_panel.SetSizer(content_sizer)
        main_sizer.Add(content_panel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

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
        wx.CallAfter(self.force_apply_styles)

    def on_button_hover(self, event, button, color):
        button.SetBackgroundColour(wx.Colour(color))
        button.Refresh()
        event.Skip()

    def on_button_leave(self, event, button, color):
        button.SetBackgroundColour(wx.Colour(color))
        button.Refresh()
        event.Skip()

    def force_apply_styles(self):
        controls = [
            self.age_input,
            self.height_input,
            self.weight_input,
            self.sex_choice,
            self.goal_choice
        ]
        for ctrl in controls:
            try:
                ctrl.SetBackgroundColour(wx.Colour(self.input_bg))
                ctrl.SetForegroundColour(wx.Colour(self.input_fg))
                ctrl.Refresh()
                ctrl.Update()
                if isinstance(ctrl, wx.ComboBox) and hasattr(ctrl, 'GetTextCtrl'):
                    text_ctrl = ctrl.GetTextCtrl()
                    if text_ctrl:
                        text_ctrl.SetBackgroundColour(wx.Colour(self.input_bg))
                        text_ctrl.SetForegroundColour(wx.Colour(self.input_fg))
                        text_ctrl.Refresh()
                        text_ctrl.Update()
            except Exception as e:
                print(f"Error styling control: {e}")

    def OnCalculate(self, event):
        try:
            if (
                    not self.age_input.GetValue().strip() or
                    not self.height_input.GetValue().strip() or
                    not self.weight_input.GetValue().strip()
            ):
                wx.MessageBox(
                    "Please fill in Age, Height, and Weight fields before calculating.",
                    "Missing Data",
                    wx.OK | wx.ICON_WARNING
                )
                return

            age = int(self.age_input.GetValue())
            height = float(self.height_input.GetValue())
            weight = float(self.weight_input.GetValue())

            if age <= 0 or height <= 0 or weight <= 0:
                wx.MessageBox(
                    "Age, Height, and Weight must be positive values.",
                    "Invalid Input",
                    wx.OK | wx.ICON_WARNING
                )
                return

            bmi = weight / (height ** 2)

            if bmi < 18.5:
                level = "Underweight"
            elif bmi < 25:
                level = "Normal"
            elif bmi < 30:
                level = "Overweight"
            else:
                level = "Obese"

            sex = self.sex_choice.GetValue()
            if sex == "Male":
                bmr = 10 * weight + 6.25 * height * 100 - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height * 100 - 5 * age - 161

            goal = self.goal_choice.GetValue()
            if goal == "Weight Loss":
                fitness_type = "Cardio Fitness"
            else:
                fitness_type = "Muscular Fitness"

            if fitness_type == "Cardio Fitness":
                activity_factor = 1.55 if goal == "Weight Loss" else 1.375
            else:
                activity_factor = 1.725 if goal == "Weight Gain" else 1.55

            tdee = bmr * activity_factor

            if goal == "Weight Loss":
                target_calories = tdee - 500
            elif goal == "Weight Gain":
                target_calories = tdee + 300
            else:
                target_calories = tdee

            self.bmi_score.SetLabel(f"{bmi:.2f}")
            self.level_score.SetLabel(level)
            self.bmr_score.SetLabel(f"{bmr:.2f}")
            self.tdee_score.SetLabel(f"{tdee:.2f}")
            self.target_calories_score.SetLabel(f"{target_calories:.2f}")
            self.act_factor_score.SetLabel(f"{activity_factor:.3f}")

            message = (
                f"Health statistics calculated successfully.\n\n\n"
                f"BMI: Body Mass Index - a measure of body fat based on height and weight\n\n"
                f"Level: Weight status category (Underweight, Normal, Overweight, or Obese)\n\n"
                f"BMR: Basal Metabolic Rate - the calories you'd burn if you stayed in bed all day\n\n"
                f"TDEE: Total Daily Energy Expenditure - all calories burned in a day including activity and exercise\n\n"
                f"Target Calories: Adjusted from TDEE to meet your fitness objective\n\n"
                f"Activity Factor: Multiplier for your activity level\n\n\n"
                f"Now click 'Generate Fitness Plan' to get your personalized recommendation."
            )
            self.result_text.SetValue(message)

            self.diet_btn.Show()
            self.diet_btn.GetParent().Layout()
            self.Layout()
            self.Refresh()

        except ValueError:
            wx.MessageBox(
                "Please enter valid numeric values for Age, Height, and Weight.",
                "Invalid Input",
                wx.OK | wx.ICON_ERROR
            )
        except Exception as e:
            wx.MessageBox(f"Input error: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def OnDiet(self, event):
        try:
            sex = 1 if self.sex_choice.GetValue() == "Male" else 0
            age = int(self.age_input.GetValue())
            height = float(self.height_input.GetValue())
            weight = float(self.weight_input.GetValue())
            hypertension = 1 if self.radio_hp_yes.GetValue() else 0
            diabetes = 1 if self.radio_d_yes.GetValue() else 0
            goal = 1 if self.goal_choice.GetValue() == "Weight Gain" else 0

            bmi = round(weight / (height ** 2), 2)

            if bmi < 18.5:
                level = 0
            elif 18.5 <= bmi < 25:
                level = 1
            elif 25 <= bmi < 30:
                level = 2
            else:
                level = 3

            fitness_type = 1 if goal == 1 else 0

            if fitness_type == 0:
                activity_factor = 1.55 if goal == 0 else 1.375
            else:
                activity_factor = 1.725 if goal == 1 else 1.55

            if sex == 1:
                bmr = 10 * weight + 6.25 * (height * 100) - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * (height * 100) - 5 * age - 161

            tdee = bmr * activity_factor
            target_calories = tdee + 300 if goal == 1 else tdee - 500

            dataframe = pd.DataFrame([{
                'Sex': sex,
                'Age': age,
                'Height': height,
                'Weight': weight,
                'Hypertension': hypertension,
                'Diabetes': diabetes,
                'BMI': bmi,
                'Level': level,
                'Fitness Goal': goal,
                'Fitness Type': fitness_type,
                'Activity Factor': activity_factor,
                'BMR': bmr,
                'TDEE': tdee,
                'Target Calories': target_calories
            }])

            FEATURES_EX = ['Age', 'Weight', 'Hypertension', 'Diabetes', 'BMI', 'Level', 'Target Calories']
            x_ex = dataframe[FEATURES_EX]
            prediction_ex = self.model_exercises.predict(x_ex)[0]
            dataframe['Exercises'] = prediction_ex

            FEATURES_DIET = [
                'Age', 'Weight', 'Hypertension', 'Diabetes', 'BMI',
                'Level', 'Exercises', 'Target Calories'
            ]
            x_diet = dataframe[FEATURES_DIET]
            prediction_diet = self.model_diet.predict(x_diet)[0]

            exercise_map = {
                0: "Squats, deadlifts, bench presses, and overhead presses",
                1: "Squats, yoga, deadlifts, bench presses, and overhead presses",
                2: "Brisk walking, cycling, swimming, running, or dancing",
                3: "Walking, yoga, swimming",
                4: "Brisk walking, cycling, swimming, or dancing"
            }

            predicted_exercises = exercise_map.get(
                prediction_ex,
                "General full body training and cardio"
            )

            vegetables, protein, juice = prediction_diet.split(';')

            diet_message = (
                f"PERSONALIZED DIET PLAN\n"
                f"{'-' * 30}\n"
                f"{vegetables}\n\n"
                f"{protein}\n\n"
                f"{juice}\n\n"
                f"RECOMMENDED EXERCISES\n"
                f"{'-' * 30}\n"
                f"{predicted_exercises}\n"
            )

            self.result_text.SetValue(diet_message)

            if self.current_user:
                try:
                    conn = sqlite3.connect('./Database/fitness_app.db')
                    cursor = conn.cursor()

                    cursor.execute(
                        """INSERT INTO diet_history 
                           (user_id, meal_type, calories, protein, carbs, fats, notes, date) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                        (self.current_user['id'], 'Dinner', 200, 11, 25, 60, vegetables)

                    )

                    cursor.execute(
                        """INSERT INTO diet_history 
                           (user_id, meal_type, calories, protein, carbs, fats, notes, date) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                        (self.current_user['id'], 'Protein Intake', 450, 40, 130, 110, protein)
                    )

                    cursor.execute(
                        """INSERT INTO diet_history 
                           (user_id, meal_type, calories, protein, carbs, fats, notes, date) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                        (self.current_user['id'], 'Other', 70, 5, 20, 40, juice)
                    )

                    cursor.execute(
                        """INSERT INTO workout_history 
                           (user_id, workout_type, duration, calories_burned, notes, date) 
                           VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                        (self.current_user['id'], 'Recommended', 30, 200, predicted_exercises)
                    )

                    conn.commit()
                    conn.close()
                except:
                    pass

        except Exception as e:
            wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def on_profile(self, event):
        try:
            from UI.profile_GUI import ProfileApp
            profile_app = ProfileApp(None, user=self.current_user)
            profile_app.Show()
            self.Close()
        except ImportError as e:
            wx.MessageBox(f"Could not open profile: {e}", "Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"Error opening profile: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_logout(self, event):
        try:
            from UI.login_GUI import LoginApp
            login_app = LoginApp(None)
            login_app.Show()
            self.Close()
        except ImportError as e:
            wx.MessageBox(f"Could not open login screen: {e}", "Error", wx.OK | wx.ICON_ERROR)


def main():
    app = wx.App(False)

    test_user = {
        'id': 1,
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com'
    }
    frame = FitnessApp(None, user=test_user)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()