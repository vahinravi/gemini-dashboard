from flask import Flask, render_template_string, request
import google.generativeai as genai

# ------------------ Gemini Setup ------------------
genai.configure(api_key="AIzaSyAPJyYQQpqdJxI1_frOLelmXM1-TlHnrFY")
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------ Flask App ------------------
app = Flask(__name__)

# --- Cloudinary Images Dictionary ---
CLOUDINARY_IMAGES = {
    "Portfolio Correlation Matrix": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754442470/fp1grvu9hmu2b9mcuoge.png",
    "Monthly Returns Heatmap": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754442469/zcz8rjlgrjwtmodq8ivl.png",
    "Fear Gauge": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754441942/vx6oolpvcbmkp3yxzhxw.png",
    "Cumulative Excess Returns vs EW Benchmark": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754442466/yqp3z0c3ibdsqd2jrvjq.png",
    "Daily Return Distributions": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754442465/ucywezln7wp2kuof80gy.png",
    "Risk Return Profile": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754442468/l4c8tzviyz7hbolhkegh.png",
    "Sentiment Final": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754441938/uswfmvckciupgxwcom0v.png",
    "Daily Weighted Sentiment": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754441940/uub4yz6ir5kicmqdesjl.png",
    "Average Annual Return": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754442462/xrpacs8snlqbls3qujpo.png",
    "Annualised Sharpe Ratios": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754442460/o0xzmaj2flzrokntpoaf.png",
    "Rolling 60 Day Volatility": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754442464/sjrstdrblhzsqqzdldom.png",
    "Rolling 60 Day Sharpe Ratio": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754442463/wmjk1xalqncw2g8v8x1r.png",
    "Cumulative Log Returns of Portfolios": "https://res.cloudinary.com/dpuaaplrt/image/upload/v1754442459/ofiqcugal7vstdnj2i8p.png",
}

# --- Grouped Query Options ---
QUERY_GROUPS = {
    "📈 Sentiment Analysis": [
        "Summarize BTC sentiment trends",
        "Explain recent sentiment-fear gauge relationship",
        "Compare crypto sentiment vs traditional markets",
        "What does the daily weighted sentiment chart mean?"
    ],
    "💹 Portfolio Performance": [
        "Explain Sharpe Ratios",
        "Summarize portfolio performance vs benchmark",
        "Describe portfolio risk-return profile",
        "Interpret the rolling 60-day volatility chart",
        "Explain the correlation matrix of portfolios"
    ],
    "📊 Strategy & Insights": [
        "What are key takeaways from the cumulative returns?",
        "How does sentiment strategy compare to BTC buy-and-hold?",
        "Provide insights on portfolio diversification benefits"
    ],
    "📚 General Finance & Crypto": [
        "Explain what risk-adjusted returns mean",
        "Describe how sentiment influences crypto prices",
        "What is the significance of fear & greed indexes?"
    ]
}

# Flatten queries for defaults
ALL_QUERIES = [q for group in QUERY_GROUPS.values() for q in group]

# ------------------ Routes ------------------
@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    selected_image = "Fear Gauge"  # Default image
    selected_query = ALL_QUERIES[0]  # Default query

    if request.method == "POST":
        if "query_type" in request.form:  # Gemini query
            selected_query = request.form.get("query_type")
            response = model.generate_content(selected_query)
            response_text = response.text
        elif "image" in request.form:  # Image button clicked
            selected_image = request.form.get("image")

    return render_template_string(
        TEMPLATE,
        query_groups=QUERY_GROUPS,
        images=CLOUDINARY_IMAGES,
        response=response_text,
        selected_image=selected_image,
        selected_query=selected_query
    )

# ------------------ HTML Template ------------------
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Crypto Dashboard with Gemini & Cloudinary</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background-color: #f8f9fa; font-family: Arial, sans-serif; }
        .container { max-width: 1000px; margin-top: 40px; }
        .card { margin-top: 20px; padding: 20px; border-radius: 12px; }
        .btn-image { margin: 4px; }
        img { max-width: 100%; border: 1px solid #ddd; border-radius: 8px; margin-top: 15px; }
        textarea { resize: none; }
        h4 { margin-bottom: 15px; }
    </style>
    <script>
        window.onload = function() {
            const resp = document.getElementById("gemini-response");
            if (resp && resp.value.trim() !== "") { resp.scrollIntoView({behavior: "smooth"}); }
            const img = document.getElementById("selected-image");
            if (img) { img.scrollIntoView({behavior: "smooth"}); }
        };
    </script>
</head>
<body>
<div class="container">
    <h1 class="text-center mb-4">🚀 Crypto Sentiment & Portfolio Dashboard</h1>

    <!-- Gemini Query Dropdown -->
    <form method="POST" class="card shadow">
        <h4>🤖 Ask Gemini</h4>
        <div class="row mb-3">
            <div class="col-10">
                <select class="form-select" name="query_type">
                    {% for group, queries in query_groups.items() %}
                    <optgroup label="{{ group }}">
                        {% for q in queries %}
                        <option value="{{ q }}" {% if q == selected_query %}selected{% endif %}>{{ q }}</option>
                        {% endfor %}
                    </optgroup>
                    {% endfor %}
                </select>
            </div>
            <div class="col-2">
                <button type="submit" class="btn btn-primary w-100">Run</button>
            </div>
        </div>
        <label><strong>Gemini Response:</strong></label>
        <textarea id="gemini-response" class="form-control" rows="5" readonly>{{ response }}</textarea>
    </form>

    <!-- Cloudinary Images -->
    <div class="card shadow">
        <h4>📊 View Portfolio & Sentiment Visuals</h4>
        <div class="mb-2">
            {% for name, url in images.items() %}
            <form method="POST" style="display:inline;">
                <input type="hidden" name="image" value="{{ name }}">
                <button type="submit" class="btn btn-outline-secondary btn-sm btn-image">{{ name }}</button>
            </form>
            {% endfor %}
        </div>
        <hr>
        <h5 class="text-center">{{ selected_image }}</h5>
        <img id="selected-image" src="{{ images[selected_image] }}" alt="{{ selected_image }}">
    </div>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
