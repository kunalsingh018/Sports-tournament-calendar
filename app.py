import gradio as gr
from genai_fetch import get_tournaments

def generate_cards(sport):
    data = get_tournaments(sport)
    if not data or "error" in data[0]:
        return f"❌ Error: {data[0]['error'] if data else 'No data found'}", ""

    cards_html = ""
    for tournament in data:
        name = tournament.get("Tournament Name", "Unknown Tournament")
        level = tournament.get("Level", "N/A")
        start_date = tournament.get("Start Date", "TBA")
        end_date = tournament.get("End Date", "TBA")
        official_url = tournament.get("Official URL", "N/A")
        streaming = tournament.get("Streaming link", "Not available")
        summary = tournament.get("Summary", "No summary available.")

        # Limit summary to 50 words
        summary_words = summary.split()
        if len(summary_words) > 50:
            summary = " ".join(summary_words[:50]) + "..."

        cards_html += f"""
        <div style="
            border: 1px solid #ddd; 
            border-radius: 15px; 
            padding: 20px; 
            margin: 15px; 
            background-color: white; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            width: 350px;
            display: inline-block;
            vertical-align: top;
            transition: transform 0.2s ease-in-out;
        " onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
            <h3 style="margin-top:0; color: #2c3e50;">{name}</h3>
            <p style="font-size: 14px; color: #555;">{summary}</p>
            <p><strong>Level:</strong> {level}</p>
            <p><strong>Start Date:</strong> {start_date}</p>
            <p><strong>End Date:</strong> {end_date}</p>
            <p><strong>Streaming:</strong> {streaming}</p>
            <p><strong>Official_url:</strong> {official_url}</p>
                
        </div>
        """

    return f"✅ Found {len(data)} tournaments", f"<div style='display:flex; flex-wrap:wrap; justify-content:center;'>{cards_html}</div>"


sports_list = [
    "Cricket", "Football", "Badminton", "Running", "Gym", "Cycling",
    "Swimming", "Kabaddi", "Yoga", "Basketball", "Chess", "Table Tennis"
]

with gr.Blocks(title="🏆 Sports Tournament Finder (Powered by Gemini)") as demo:
    gr.Markdown("## 🏆 Sports Tournament Finder\nSelect a sport and click **Search Tournament** to see upcoming events in India.")

    with gr.Row():
        sport_dropdown = gr.Dropdown(sports_list, label="Select Sport", scale=1)
        search_btn = gr.Button("🔍 Search Tournament", scale=0)

    status_text = gr.Textbox(label="Status", interactive=False)
    tournament_cards = gr.HTML()

    search_btn.click(
        fn=generate_cards,
        inputs=sport_dropdown,
        outputs=[status_text, tournament_cards]
    )

demo.launch()
