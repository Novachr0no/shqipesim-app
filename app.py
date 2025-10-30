import streamlit as st
from datetime import datetime

# Abbreviation map
shkurtime = {
    "flm": "faleminderit",
    "ntn": "natën e mirë",
    "skgj": "s’ka gjë",
    "mf": "më fal",
    "klm": "kalo mirë",
    "shnet": "shëndet",
    "psejo": "pse jo",
    "pojo": "pse jo",
    "sje": "s’je",
    "sjam": "s’jam",
    "tltm": "të lutem",
    "kk": "okey",
    "pr": "për",
    "rrfsh": "rrofsh",
    "cpb": "ca po bën",
    "ber": "bërë",
}

# --- Helper function ---
def detect_and_replace(text):
    words = text.split()
    corrected = []
    found = []
    for w in words:
        prefix, suffix, core = "", "", w
        # Handle punctuation
        while len(core) and not core[0].isalnum():
            prefix += core[0]
            core = core[1:]
        while len(core) and not core[-1].isalnum():
            suffix = core[-1] + suffix
            core = core[:-1]

        lw = core.lower()
        if lw in shkurtime:
            replacement = shkurtime[lw]
            corrected.append(prefix + replacement + suffix)
            found.append((w, replacement))
        else:
            corrected.append(w)

    corrected_text = " ".join(corrected)
    total = len(words)
    slang = len(found)
    score = round(((total - slang) / total) * 100, 1) if total > 0 else 100.0
    return found, corrected_text, score


# --- Streamlit UI ---
st.set_page_config(page_title="🗣️ Shqip e Pastër", layout="centered")
st.title("🗣️ Shqip e Pastër — Kontrollo & Korrigjo")
st.caption("Detekton dhe zëvendëson shkurtimet më të zakonshme në shqip.")

# Input area
user_text = st.text_area(
    "Shkruaj një fjali me shkurtimet që do të korrigjohen:",
    placeholder="p.sh. flm qe erdhe ntn...",
    height=140,
)

if st.button("Analizo tekstin"):
    if not user_text.strip():
        st.warning("Ju lutem shkruani tekst për të analizuar.")
    else:
        found, corrected, score = detect_and_replace(user_text)
        st.subheader("Rezultati")

        st.write("**Teksti origjinal:**")
        st.write(user_text)

        if found:
            st.write(f"**✅ U gjetën {len(found)} shkurtime:**")
            for o, r in found:
                st.write(f"- `{o}` → **{r}**")
        else:
            st.write("**🎉 Asnjë shkurtime nuk u gjet!**")

        st.write("**🔤 Teksti i korrigjuar:**")
        st.code(corrected, language="text")

        st.write(f"**💯 Gjuha e pastër:** {score}%")

st.write("---")
st.caption("Krijuar për të inkurajuar përdorimin e gjuhës standarde shqipe 🇦🇱")
