import streamlit as st

# =========================================================
#  HAPPY 18TH BIRTHDAY, ARYA — a little app made by Viraj
# =========================================================

st.set_page_config(
    page_title="Happy Birthday Arya",
    page_icon="🎈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
#  SESSION STATE
# ---------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "quiz_revealed" not in st.session_state:
    st.session_state.quiz_revealed = [False] * 8
if "surprise_revealed" not in st.session_state:
    st.session_state.surprise_revealed = [False] * 8

PAGES = ["home", "letter", "quiz", "surprise"]
PAGE_LABELS = {"home": "Home", "letter": "The Letter", "quiz": "The Quiz", "surprise": "The Surprise"}

# ---------------------------------------------------------
#  DECORATIVE SVG ASSETS
# ---------------------------------------------------------

BALLOON_SVG = """
<svg width="230" height="270" viewBox="0 0 230 270" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;">
  <path d="M62 152 Q40 205 57 248" stroke="#C9A24B" stroke-width="1.6" fill="none"/>
  <path d="M115 164 Q104 214 110 256" stroke="#9B1B32" stroke-width="1.6" fill="none"/>
  <path d="M168 152 Q184 205 165 248" stroke="#C4444E" stroke-width="1.6" fill="none"/>
  <ellipse cx="62" cy="96" rx="44" ry="55" fill="#C4444E"/>
  <ellipse cx="46" cy="74" rx="12" ry="16" fill="#ffffff" opacity="0.22"/>
  <ellipse cx="115" cy="82" rx="49" ry="61" fill="#9B1B32"/>
  <ellipse cx="97" cy="58" rx="13" ry="18" fill="#ffffff" opacity="0.22"/>
  <ellipse cx="168" cy="99" rx="42" ry="52" fill="#C9A24B"/>
  <ellipse cx="153" cy="77" rx="11" ry="15" fill="#ffffff" opacity="0.3"/>
</svg>
"""

def flower_svg(size=34, gap=44):
    half = gap / 2
    return f"""
    <svg width="100%" height="{size}" viewBox="0 0 320 {size}" preserveAspectRatio="none"
         xmlns="http://www.w3.org/2000/svg">
      <line x1="0" y1="{size/2}" x2="{160-half}" y2="{size/2}" stroke="#C9A24B" stroke-width="1"/>
      <line x1="{160+half}" y1="{size/2}" x2="320" y2="{size/2}" stroke="#C9A24B" stroke-width="1"/>
      <g transform="translate(160,{size/2})">
        <circle cx="0" cy="-9" r="6" fill="#C4444E"/>
        <circle cx="8" cy="-3" r="6" fill="#C4444E"/>
        <circle cx="5" cy="7" r="6" fill="#C4444E"/>
        <circle cx="-5" cy="7" r="6" fill="#C4444E"/>
        <circle cx="-8" cy="-3" r="6" fill="#C4444E"/>
        <circle cx="0" cy="0" r="5" fill="#C9A24B"/>
      </g>
    </svg>
    """

CORNER_BLOOM = """
<svg width="46" height="46" viewBox="0 0 46 46" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(23,23)">
    <circle cx="0" cy="-11" r="8" fill="#F5D9DA"/>
    <circle cx="10" cy="-4" r="8" fill="#F5D9DA"/>
    <circle cx="6" cy="9" r="8" fill="#F5D9DA"/>
    <circle cx="-6" cy="9" r="8" fill="#F5D9DA"/>
    <circle cx="-10" cy="-4" r="8" fill="#F5D9DA"/>
    <circle cx="0" cy="0" r="7" fill="#C9A24B"/>
  </g>
</svg>
"""

# ---------------------------------------------------------
#  GLOBAL STYLE
# ---------------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Jost:wght@300;400;500;600&display=swap');

:root{
  --cream:#FFF7F1;
  --paper:#FFFDFB;
  --deep-red:#9B1B32;
  --soft-red:#C4444E;
  --blush:#F5D9DA;
  --gold:#C9A24B;
  --ink:#2E1A1D;
}

#MainMenu, footer, header {visibility:hidden;}

.stApp{
  background:
    radial-gradient(circle at 8% 8%, rgba(155,27,50,0.05), transparent 40%),
    radial-gradient(circle at 92% 85%, rgba(201,162,75,0.07), transparent 42%),
    var(--cream);
}

.block-container{
  max-width: 740px;
  padding-top: 1.6rem;
  padding-bottom: 3rem;
}

html, body, [class*="css"]{
  font-family: 'Jost', sans-serif;
  color: var(--ink);
}

h1,h2,h3, .display-font{
  font-family: 'Playfair Display', serif;
}

/* ---- nav pills (st.radio) ---- */
div[data-testid="stRadio"] > label { display:none; }
div[data-testid="stRadio"] > div[role="radiogroup"]{
  display:flex;
  justify-content:center;
  gap:0.6rem;
  flex-wrap: wrap;
  margin-bottom: 1.2rem;
}
div[data-testid="stRadio"] label{
  border:1.4px solid var(--soft-red);
  border-radius: 30px;
  padding: 0.35rem 1.1rem;
  cursor:pointer;
  background: var(--paper);
  transition: all .18s ease;
}
div[data-testid="stRadio"] label:hover{
  background: var(--blush);
}
div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p{
  font-size: 0.92rem;
  color: var(--deep-red);
  font-weight: 500;
  letter-spacing: 0.01em;
}
div[data-testid="stRadio"] input{ display:none; }
div[data-testid="stRadio"] label:has(input:checked){
  background: var(--deep-red);
  border-color: var(--deep-red);
}
div[data-testid="stRadio"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p{
  color: var(--paper);
}

/* ---- buttons ---- */
div.stButton > button{
  background: var(--paper);
  border: 1.4px solid var(--soft-red);
  color: var(--deep-red);
  border-radius: 10px;
  font-family: 'Jost', sans-serif;
  font-weight: 500;
  padding: 0.5rem 1rem;
  transition: all .18s ease;
}
div.stButton > button:hover{
  background: var(--deep-red);
  color: var(--paper);
  border-color: var(--deep-red);
}
div.stButton > button:active{
  transform: scale(0.98);
}

/* ---- headline ---- */
.hero-title{
  text-align:center;
  color: var(--deep-red);
  font-size: clamp(2.1rem, 6vw, 3.3rem);
  font-weight: 700;
  letter-spacing: 0.01em;
  margin: 0.6rem 0 0.2rem 0;
  line-height: 1.15;
}
.hero-sub{
  text-align:center;
  color: var(--ink);
  font-style: italic;
  font-size: 1.05rem;
  opacity: 0.85;
  margin-bottom: 0.4rem;
}
.lead-text{
  text-align:center;
  font-size: 1rem;
  line-height: 1.75;
  max-width: 520px;
  margin: 0.6rem auto 0 auto;
  opacity: 0.9;
}

/* ---- scroll for the letter ---- */
.scroll-wrap{ position: relative; margin-top: 1.2rem; }
.scroll{
  background: var(--paper);
  border-radius: 18px;
  padding: 2.4rem 2.2rem;
  box-shadow:
    0 1px 0 var(--gold),
    0 22px 45px -20px rgba(155,27,50,0.25),
    inset 0 0 0 1px rgba(201,162,75,0.35);
  position: relative;
}
.scroll-heading{
  text-align:center;
  color: var(--deep-red);
  font-size: 1.6rem;
  margin-bottom: 0.8rem;
}
.scroll-text{
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.28rem;
  line-height: 1.95;
  color: var(--ink);
  text-align: left;
}
.corner{ position:absolute; opacity:0.9; }
.corner.tl{ top:-14px; left:-14px; }
.corner.br{ top: auto; bottom:-14px; right:-14px; transform: rotate(180deg); }

/* ---- quiz cards ---- */
.q-card{
  background: var(--paper);
  border-left: 4px solid var(--deep-red);
  border-radius: 10px;
  padding: 1.1rem 1.3rem 0.9rem 1.3rem;
  margin-bottom: 1.1rem;
  box-shadow: 0 8px 20px -14px rgba(0,0,0,0.25);
}
.q-text{
  font-weight: 600;
  font-size: 1.02rem;
  margin-bottom: 0.7rem;
  color: var(--ink);
}
.q-reveal{
  margin-top: 0.7rem;
  background: var(--blush);
  border-radius: 8px;
  padding: 0.55rem 0.9rem;
  color: var(--deep-red);
  font-weight: 600;
  font-size: 0.96rem;
}

/* ---- surprise ---- */
.surprise-title{
  text-align:center;
  color: var(--deep-red);
  font-size: clamp(2rem, 7vw, 3rem);
  font-weight: 700;
  margin-bottom: 0.1rem;
}
.surprise-sub{
  text-align:center;
  font-style: italic;
  opacity: 0.85;
  margin-bottom: 1.6rem;
}
.final-reveal{
  text-align:center;
  font-family: 'Playfair Display', serif;
  font-size: 1.35rem;
  color: var(--deep-red);
  margin-top: 1.8rem;
  animation: fadeIn 1.1s ease;
}
@keyframes fadeIn{
  from{ opacity:0; transform: translateY(8px); }
  to{ opacity:1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
#  NAVIGATION
# ---------------------------------------------------------

current_index = PAGES.index(st.session_state.page)
choice = st.radio(
    "nav",
    PAGES,
    index=current_index,
    format_func=lambda p: PAGE_LABELS[p],
    horizontal=True,
    label_visibility="collapsed",
    key="nav_radio",
)
st.session_state.page = choice

# ---------------------------------------------------------
#  HOME PAGE
# ---------------------------------------------------------

def render_home():
    st.markdown(BALLOON_SVG, unsafe_allow_html=True)
    st.markdown('<div class="hero-title">HAPPY BIRTHDAY ARYA!!!!</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">eighteen candles, one incredible girl</div>', unsafe_allow_html=True)
    st.markdown(flower_svg(), unsafe_allow_html=True)
    st.markdown(
        '<div class="lead-text">Three little corners of this day are waiting for you — '
        'a letter, a quiz only you can win, and one last surprise. '
        'Take your time, princess, today is entirely yours.</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
#  LETTER PAGE
# ---------------------------------------------------------

LOVE_LETTER = (
    "HAPPY 18TH BIRTHDAY ARYAAAAAAAAA, many many happy returns of the day, i am so insanely "
    "excited that the 15th year old that i used to love has turned 18, today is a huge day, i "
    "hope you like the stuff i have made for you, i love you so much aaru, today is your day, "
    "and all i wish for is your happiness, you are the person that cares about everyone's "
    "birthday, and so this is the least you deserve, the love of my life turning 18 is such an "
    "unimaginable feeling for me, the lil girl i used to see everyday in tutions is all grown up "
    "ab, it has been beautiful seeing you grow up so much, you are a beautiful smart and quirky "
    "lady and i love that so much about you, you are the type of person that never ever gets "
    "boring, i always love being with you, even before we started dating, when we were just "
    "friends, i never once felt that i shoudlnt talk to you, it was always so fun being with you, "
    "as a friend and as a boyfriend, but dont you ever forget, aap kitni bhi badi ho jao, rahoge "
    "toh aap mere lil cutie patootie girlie hi ha, i love you so so so so muchhhh, i will always "
    "love you kiko, no matter what, once again princess, many many happy returns of the day, and "
    "i hope you have funnnn, i love youuuuuuu."
)

def render_letter():
    st.markdown('<h2 class="hero-title" style="font-size:2rem;">For Arya</h2>', unsafe_allow_html=True)
    st.markdown(flower_svg(size=28), unsafe_allow_html=True)
    st.markdown('<div class="scroll-wrap">', unsafe_allow_html=True)
    st.markdown(f'<div class="corner tl">{CORNER_BLOOM}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="corner br">{CORNER_BLOOM}</div>', unsafe_allow_html=True)
    st.markdown('<div class="scroll">', unsafe_allow_html=True)
    st.markdown('<div class="scroll-heading">A little letter, just for you</div>', unsafe_allow_html=True)
    st.markdown('<p class="scroll-text">' + LOVE_LETTER + "</p>", unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
#  QUIZ PAGE
# ---------------------------------------------------------

QUIZ = [
    ("WHO IS THE BIRTHDAY GIRLLLLLLLL", "ARYA", "THE ONE AND ONLYYY"),
    ("who likes pitza more", "ARYA", "(obviously, tho thats not the surprise hehe)"),
    ("the baddie who is going to slay in a hot red dress today", "VIRAJ", "(hahahahaha)"),
    ("who was roaming the enitre airport with soapy hands", "ARYA", "(HAHAHAHAHHAHA)"),
    ("who is the BOSS", "ARYA", "(undisputed)"),
    ("who is everyone's favvvv", "ARYA", "(OBVIOUSLYYYY)"),
    ("who is better at hindi", "VIRAJ", "(ez)"),
    ("who doesnt know the surprise gift yetttt", "ARYA", "(turn to the next page M'lady)"),
]

def render_quiz():
    st.markdown('<h2 class="hero-title" style="font-size:2rem;">A Few Questions, Just For Fun</h2>', unsafe_allow_html=True)
    st.markdown(flower_svg(size=28), unsafe_allow_html=True)
    for i, (question, answer, flavor) in enumerate(QUIZ):
        st.markdown('<div class="q-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="q-text">{i+1}. {question}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("ARYA", key=f"arya_{i}", use_container_width=True):
                st.session_state.quiz_revealed[i] = True
        with c2:
            if st.button("VIRAJ", key=f"viraj_{i}", use_container_width=True):
                st.session_state.quiz_revealed[i] = True
        if st.session_state.quiz_revealed[i]:
            st.markdown(f'<div class="q-reveal">{answer} — {flavor}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
#  SURPRISE PAGE
# ---------------------------------------------------------

WORD = ["M", "A", "G", "A", "Z", "I", "N", "E"]

def render_surprise():
    st.markdown('<div class="surprise-title">SURPRISEEEEE</div>', unsafe_allow_html=True)
    st.markdown('<div class="surprise-sub">you have lost the ability to surprise me</div>', unsafe_allow_html=True)

    cols = st.columns(8)
    for i, col in enumerate(cols):
        with col:
            label = WORD[i] if st.session_state.surprise_revealed[i] else "?"
            if st.button(label, key=f"box_{i}", use_container_width=True):
                st.session_state.surprise_revealed[i] = True

    if all(st.session_state.surprise_revealed):
        st.markdown(
            '<div class="final-reveal">are you sure i have lost the ability to surprise you baby doll</div>',
            unsafe_allow_html=True,
        )
        st.balloons()

# ---------------------------------------------------------
#  ROUTER
# ---------------------------------------------------------

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "letter":
    render_letter()
elif st.session_state.page == "quiz":
    render_quiz()
elif st.session_state.page == "surprise":
    render_surprise()
