import openai
import gradio as gr
import datetime
import calendar


openai.api_key = ""

messages = [{"role": "system", "content": "You are a medical wellbeing expert that specialises in helping parents deal with stress and wellbeing of themselves."}]
tasks = {}

def CustomChatGPT(user_input):
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ChatGPT_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": ChatGPT_reply})
        return [[user_input, ChatGPT_reply]]
    except Exception as e:
        print(f"Error: {str(e)}")
        return [[user_input, f"Error: {str(e)}"]]

def clear_chat():
    global messages
    messages = [{"role": "system", "content": "You are a medical wellbeing expert that specialises in helping parents deal with stress and wellbeing of themselves."}]
    return []

def switch_tab(tab_name):
    if tab_name == "home":
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    elif tab_name == "chat":
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

def add_task(date_str, task):
    if not task.strip():
        return update_calendar()
    if date_str not in tasks:
        tasks[date_str] = []
    tasks[date_str].append(task)
    print(f"Added task '{task}' for date {date_str}")  # Debug print
    print(f"Current tasks: {tasks}")  # Debug print
    return generate_calendar_html()

def generate_calendar_html():
    current_date = datetime.datetime.now()
    month_days = calendar.monthcalendar(current_date.year, current_date.month)
    
    day_cells = []
    for week in month_days:
        week_html = []
        for day in week:
            if day == 0:
                week_html.append('<div class="calendar-day"></div>')
                continue
                
            date_str = f"{current_date.year}-{current_date.month:02d}-{day:02d}"
            day_tasks = tasks.get(date_str, [])
            task_html = ''
            if day_tasks:
                task_html = '<div class="sticky-note">'
                task_html += '<br>'.join(day_tasks)
                task_html += '</div>'
            
            is_current = current_date.day == day
            week_html.append(f'''
                <div class="calendar-day{' current-day' if is_current else ''}">
                    <span>{day}</span>
                    {task_html}
                </div>
            ''')
        day_cells.append(f'<div class="calendar-week">{"".join(week_html)}</div>')
    
    return f'''
        <div class="calendar">
            <div class="calendar-header">
                <h3>{calendar.month_name[current_date.month]} {current_date.year}</h3>
            </div>
            <div class="calendar-grid">
                <div class="calendar-weekdays">
                    <span>Sun</span><span>Mon</span><span>Tue</span>
                    <span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span>
                </div>
                {"".join(day_cells)}
            </div>
        </div>
    '''

def update_calendar():
    return generate_calendar_html()

def get_current_month_dates():
    current_date = datetime.datetime.now()
    days = calendar.monthcalendar(current_date.year, current_date.month)
    dates = []
    for week in days:
        for day in week:
            if day != 0:
                date_str = f"{current_date.year}-{current_date.month:02d}-{day:02d}"
                dates.append(date_str)
    return dates

custom_css = """

     @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Base colors */
    :root {
        --primary: #FF9F67;         /* Warm orange */
        --secondprimary: #6684A0;
        --secondary: #FFB085;       /* Soft peach */
        --accent: #FFD699;          /* Muted yellow */
        --background: #FFF5EB;      /* Cream white */
        --text-dark: #4A4036;       /* Warm brown */
        --text-light: #8C7B6B;      /* Light brown */
        --note-color: #FFE5CC;      /* Soft peach for sticky notes */
        --highlight: #FF7F50;       /* Coral highlight */


        /* Typography scale */
        --font-xs: 0.75rem;         /* 12px */
        --font-sm: 0.875rem;        /* 14px */
        --font-base: 1rem;          /* 16px */
        --font-lg: 1.125rem;        /* 18px */
        --font-xl: 1.25rem;         /* 20px */
        --font-2xl: 1.5rem;         /* 24px */
        --font-3xl: 2rem;           /* 32px */
        --font-4xl: 2.5rem;         /* 40px */
    }

    /* Global font settings */
    * {
        font-family: 'Outfit', sans-serif;
        line-height: 1.5;
    }

    .calendar-day {
        min-height: 80px !important;
        padding: 5px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    .sticky-note {
        background: #fff7b6;
        padding: 8px;
        border-radius: 4px;
        font-size: 12px;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-top: 5px;
        width: 90%;
        text-align: left;
    }

    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
        padding-top: 0 !important;
        background: linear-gradient(180deg, var(--primary) 0%, var(--background) 100%) !important;
        min-height: 100vh !important;
    }

    .nav-bar {
        background: var(--primary);
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 4px rgba(74, 64, 54, 0.1);
    }
    
    .nav-brand {
        font-size: var(--font-2xl);
        font-weight: 600;
        color: var(--background);
    }
    
    .nav-buttons {
        display: flex;
        gap: 1rem;
    }
    
    .nav-link {
        font-size: var(--font-base) !important;
        font-weight: 500 !important;
    }
    
    .nav-link:hover {
    background: rgba(0, 0, 255, 0.2) !important; /* Blue with 20% opacity */
    }

    .nav-logo {
    width: 24px; /* Adjust the size */
    height: 24px; /* Adjust the size */
    vertical-align: middle; /* Align with text */
    margin-right: 8px; /* Add space after the image */
}
    
    .progress-section {
        background: var(--background);
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(74, 64, 54, 0.1);
        padding: 20px;
        margin: 20px auto;
        max-width: 800px;
    }
    
    .progress-title {
        font-size: var(--font-lg);
        font-weight: 600;
    }
    
    .week-progress {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-top: 15px;
    }
    
    .day-progress {
        flex: 1;
        text-align: center;
    }
    
    .progress-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: var(--accent);
        margin: 0 auto 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: var(--text-dark);
        
    }
    
    .progress-circle.completed {
        background: #cce5ff !important;
        color: var(--text-dark);
    
    }
    
    .progress-label {
        font-size: var(--font-sm);
        font-weight: 500;
    }

    .calendar {
        background: var(--background);
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(74, 64, 54, 0.1);
        padding: 30px;
        margin: 20px auto;
        max-width: 1000px;
        width: 100%;
    }
    
    .calendar-header {
        text-align: center;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 20px;
    }
    
    .calendar-header h3 {
        font-size: var(--font-2xl);
        font-weight: 600;
    }
    
    .calendar-grid {
        width: 100%;
    }
    
    .calendar-weekdays {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    text-align: center;
    font-size: var(--font-sm);
    font-weight: 600;
    margin-bottom: 10px; /* Add spacing between weekdays and the grid */
}
    
    .calendar-week {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        text-align: center;
        
    }
    
    .calendar-day {
    font-size: var(--font-base);
    font-weight: 400;
    min-height: 80px; /* Ensure consistent height */
    display: flex; /* Center content within each day */
    align-items: center;
    justify-content: center;
    padding: 5px;
}
    
    .calendar-day:hover {
        background-color: var(--accent);
    }
    
    .current-day {
        font-weight: 600;
    }

    #chat_window {
        height: 600px !important;
        background: rgba(255, 245, 235, 0.95) !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 12px rgba(74, 64, 54, 0.08) !important;
        margin: 1rem !important;
        padding: 1rem !important;
    }
    
    #chat_window .message {
        font-size: var(--font-base) !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
    }
    
    #chat_window .user {
        background: var(--accent) !important;
        margin-left: auto !important;
        border-bottom-right-radius: 4px !important;
    }
    
    #chat_window .bot {
    background: #cce5ff !important; /* Light blue background /
    color: #004085 !important;      / Dark blue text color /
    border: 1px solid #b8daff !important; / Light blue border /
    margin-right: auto !important;
    border-bottom-left-radius: 4px !important;
    padding: 10px; / Optional for spacing */
}

    #user_input {
        border-radius: 10px !important;
        border: 2px solid var(--primary) !important;
        background: white !important;
        margin: 1rem !important;
    }

    #submit_button, #clear_button {
        background: var(--primary) !important;
        border: none !important;
        color: var(--background) !important;
        border-radius: 8px !important;
        padding: 0.8rem 1.5rem !important;
        margin: 0.5rem !important;
        transition: all 0.3s ease !important;
    }

    #submit_button:hover, #clear_button:hover {
        background: var(--highlight) !important;
        transform: translateY(-2px) !important;
    }

    .header {
        padding: 2rem;
        text-align: center;
        color: var(--text-dark);
    }

    .header h1 {
        font-size: var(--font-4xl);
        font-weight: 700;
        line-height: 1.2;
    }

    .header p {
        font-size: var(--font-lg);
        font-weight: 400;
        line-height: 1.6;
    }

    .section-container {
        padding: 1rem;
        transition: all 0.3s ease;
    }

    .todo-container {
        background: var(--background);
        border-radius: 12px;
        padding: 20px;
        margin-left: 20px;
        width: 250px;
    }
"""

with gr.Blocks(css=custom_css) as demo:
    with gr.Row(elem_classes="nav-bar"):
        
        with gr.Row(elem_classes="nav-buttons"):
            home_btn = gr.Button("Home", elem_classes="nav-link")
            chat_btn = gr.Button("Chat", elem_classes="nav-link")
            community_btn = gr.Button("Community", elem_classes="nav-link")

    gr.HTML("""
        <div class="header">
            <h1>Welcome to ParentPulse</h1>
            <p>Your personalized parenting assistant</p>
        </div>
    """)

    with gr.Column(visible=True, elem_id="home-section", elem_classes="section-container") as home_section:
        gr.HTML("""
            <div class="progress-section">
                <h3 class="progress-title">7-Day Progress</h3>
                <div class="week-progress">
                    <div class="day-progress">
                        <div class="progress-circle completed">M</div>
                        <div class="progress-label">Mon</div>
                    </div>
                    <div class="day-progress">
                        <div class="progress-circle completed">T</div>
                        <div class="progress-label">Tue</div>
                    </div>
                    <div class="day-progress">
                        <div class="progress-circle">W</div>
                        <div class="progress-label">Wed</div>
                    </div>
                    <div class="day-progress">
                        <div class="progress-circle">T</div>
                        <div class="progress-label">Thu</div>
                    </div>
                    <div class="day-progress">
                        <div class="progress-circle">F</div>
                        <div class="progress-label">Fri</div>
                    </div>
                    <div class="day-progress">
                        <div class="progress-circle">S</div>
                        <div class="progress-label">Sat</div>
                    </div>
                    <div class="day-progress">
                        <div class="progress-circle">S</div>
                        <div class="progress-label">Sun</div>
                    </div>
                </div>
            </div>
        """)
        
        with gr.Row():
            calendar_display = gr.HTML(update_calendar())
            with gr.Column(elem_classes="todo-container"):
                selected_date = gr.Dropdown(
        label="Select Date", 
        choices=get_current_month_dates(),
        value=datetime.datetime.now().strftime("%Y-%m-%d")
    )
                task_input = gr.Textbox(label="New Task", placeholder="Enter task...")
                add_task_btn = gr.Button("Add Task", variant="primary")

        add_task_btn.click(
            fn=add_task,
            inputs=[selected_date, task_input],
            outputs=[calendar_display]
        ).then(
            fn=lambda: "",
            outputs=[task_input]
        )

    with gr.Column(visible=False, elem_id="chat-section", elem_classes="section-container") as chat_section:
        chatbot = gr.Chatbot(
            label="Chat",
            elem_id="chat_window",
            layout="bubble",
            height=600,
            container=True,
            bubble_full_width=False,
            show_label=False
        )
        with gr.Row():
            with gr.Column(scale=8):
                user_input = gr.Textbox(
                    placeholder="Ask a parenting question...",
                    label="",
                    lines=2,
                    elem_id="user_input",
                    container=False,
                    show_label=False
                )
            with gr.Column(scale=2):
                with gr.Row():
                    submit_button = gr.Button("Send", elem_id="submit_button")
                    clear_button = gr.Button("Clear", elem_id="clear_button")

    with gr.Column(visible=False, elem_id="community-section", elem_classes="section-container") as community_section:
        gr.HTML("""
            <div class="calendar">
                <h2>Community Features Coming Soon!</h2>
                <p>Stay tuned for exciting community features and discussions.</p>
            </div>
        """)

    home_btn.click(
        fn=lambda: switch_tab("home"),
        outputs=[home_section, chat_section, community_section]
    )
    
    chat_btn.click(
        fn=lambda: switch_tab("chat"),
        outputs=[home_section, chat_section, community_section]
    )
    
    community_btn.click(
        fn=lambda: switch_tab("community"),
        outputs=[home_section, chat_section, community_section]
    )

    submit_button.click(
        fn=CustomChatGPT,
        inputs=user_input,
        outputs=chatbot
    ).then(
        fn=lambda: "",
        outputs=user_input
    )

    clear_button.click(
        clear_chat,
        inputs=None,
        outputs=chatbot,
        queue=False
    )

    user_input.submit(
        fn=CustomChatGPT,
        inputs=user_input,
        outputs=chatbot
    ).then(
        fn=lambda: "",
        outputs=user_input
    )

demo.launch(share=True)