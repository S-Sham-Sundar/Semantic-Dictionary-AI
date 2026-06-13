// =============================================
// script.js — Semantic Dictionary AI
// Handles: search, API call, rendering results,
//          algorithm badges, info modals,
//          architecture panel toggle.
// =============================================


// =============================================
// SECTION 1: ALGORITHM INFO DATA
// Each entry drives:
//   - The badge label shown on every card
//   - The badge CSS class (for colour)
//   - The modal popup content when [i] is clicked
// =============================================

const ALGO_INFO = {

    definition: {
        label:      "Dictionary API",
        badgeClass: "badge-dict",
        title:      "Dictionary API",
        purpose:    "Fetches human-readable definitions, parts of speech, synonyms, and antonyms for the queried word from an external dictionary data source.",
        complexity: "O(1) — HTTP request, no local computation",
        pipeline: [
            "User query",
            "HTTP GET → Dictionary API",
            "Parse JSON response",
            "Extract definition + word forms"
        ],
        note: "Acts as the linguistic grounding layer. Even when the other algorithms find related words, the Dictionary layer confirms authoritative meaning."
    },

    autocomplete: {
        label:      "Trie",
        badgeClass: "badge-trie",
        title:      "Trie Data Structure",
        purpose:    "A Trie (prefix tree) stores all ~99K words. Each character is a node. Looking up 'oce' instantly returns all words that start with those letters.",
        complexity: "O(k) — where k is the length of the prefix",
        pipeline: [
            "User prefix (e.g. 'oce')",
            "Walk Trie node by node",
            "Collect all words under matching subtree",
            "Return top-N suggestions"
        ],
        note: "Far more efficient than scanning a flat word list (O(n)). This is a classic DSA data structure — a must-know for interviews."
    },

    fuzzy: {
        label:      "Levenshtein",
        badgeClass: "badge-lev",
        title:      "Levenshtein Distance",
        purpose:    "Measures how many single-character edits (insertions, deletions, substitutions) are needed to turn one word into another. Used to find near-matches when the user makes a typo.",
        complexity: "O(m × n) — dynamic programming on two strings of length m and n",
        pipeline: [
            "User query (possibly misspelled)",
            "Compare against word list using edit distance",
            "Filter words within threshold (e.g. distance ≤ 2)",
            "Return closest matches"
        ],
        note: "Implemented with a 2D DP table. The same algorithm powers spell-checkers, DNA sequence alignment, and Git's diff."
    },

    semantic: {
        label:      "FAISS + Embeddings",
        badgeClass: "badge-faiss",
        title:      "FAISS Vector Search",
        purpose:    "Encodes words into high-dimensional vectors using a SentenceTransformer model. FAISS (Facebook AI Similarity Search) then finds the nearest vectors — words that are semantically close even if they look nothing alike.",
        complexity: "O(log n) — approximate nearest neighbour index",
        pipeline: [
            "Query word",
            "SentenceTransformer → 384-dim embedding",
            "FAISS ANN index search",
            "Return top-K similar word vectors"
        ],
        note: "Unlike synonyms (same meaning) or fuzzy matches (similar spelling), FAISS finds contextual relatives — e.g. 'ocean' might return 'tidal', 'maritime', 'abyssal'."
    },

    graph: {
        label:      "BFS Graph",
        badgeClass: "badge-graph",
        title:      "Semantic Graph + BFS",
        purpose:    "A graph of ~99,000 word nodes and ~396,000 edges connects semantically related words. Breadth-First Search traverses this graph outward from the query word, collecting neighbours at each hop.",
        complexity: "O(V + E) — BFS on a graph with V vertices and E edges",
        pipeline: [
            "Query word → find graph node",
            "Initialise BFS queue with that node",
            "Visit neighbours level by level",
            "Collect words within N hops",
            "Return traversal results"
        ],
        note: "BFS guarantees shortest-path order — words found at hop 1 are more closely related than words at hop 3. The graph encodes real linguistic relationships."
    },

    synonyms: {
        label:      "Dictionary API",
        badgeClass: "badge-dict",
        title:      "Synonyms (Dictionary API)",
        purpose:    "Synonyms are extracted directly from the Dictionary API response. These are official lexicographic synonyms — words with the same or very similar meaning.",
        complexity: "O(1) — parsed from the same API call as the definition",
        pipeline: [
            "Dictionary API response",
            "Extract 'synonyms' field",
            "Render as tags"
        ],
        note: "Compare with FAISS Semantic Search: synonyms are hand-curated dictionary entries, while FAISS finds contextual neighbours via ML embeddings."
    },

    antonyms: {
        label:      "Dictionary API",
        badgeClass: "badge-dict",
        title:      "Antonyms (Dictionary API)",
        purpose:    "Antonyms are also sourced from the Dictionary API — official opposites as defined by lexicographers.",
        complexity: "O(1) — parsed from the same API call as the definition",
        pipeline: [
            "Dictionary API response",
            "Extract 'antonyms' field",
            "Render as neutral tags"
        ],
        note: "Antonyms complement semantic understanding. Combined with synonyms and graph traversal, they reveal a word's full meaning space."
    },

    // ---- NEW: Gemini AI Explanation entry ----
    ai_explanation: {
        label:      "Gemini 2.5 Flash",
        badgeClass: "badge-gemini",
        title:      "Gemini 2.5 Flash — Generative AI",
        purpose:    "Generates a contextual, human-readable explanation using retrieved information from the dictionary layer, FAISS semantic search results, and graph traversal output. This is the RAG (Retrieval-Augmented Generation) layer of the system.",
        complexity: "LLM Inference — O(n) in token count, hardware-dependent",
        pipeline: [
            "Query + Retrieved Context (Dict + FAISS + Graph)",
            "Build structured prompt for Gemini",
            "Gemini 2.5 Flash inference",
            "Stream / return explanation text",
            "Render with typewriter animation"
        ],
        note: "This layer transforms raw retrieved data into human understanding. Unlike the other layers that return word lists, Gemini synthesises across all sources to explain meaning, context, and connections in natural language."
    }
};


// =============================================
// SECTION 2: KEYBOARD SHORTCUT
// Press Enter in the input to trigger search.
// =============================================

document.getElementById("query").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        searchWord();
    }
});


// =============================================
// SECTION 3: UI STATE HELPERS
// Clean functions to show/hide UI states.
// =============================================

function setLoading(isLoading) {
    const loader = document.getElementById("loading");
    if (isLoading) {
        loader.classList.remove("hidden");
    } else {
        loader.classList.add("hidden");
    }
}

function setError(hasError) {
    const errorBox = document.getElementById("error-message");
    if (hasError) {
        errorBox.classList.remove("hidden");
    } else {
        errorBox.classList.add("hidden");
    }
}

// Hide the empty state once a search has been made
function hideEmptyState() {
    const empty = document.getElementById("empty-state");
    if (empty) empty.style.display = "none";
}


// =============================================
// SECTION 4: TAG LIST RENDERER
// Renders an array of strings as pill chips.
// tagClass: "tag" (accent) or "tag-neutral" (muted)
// emptyText: fallback if array is empty
// =============================================

function renderTags(items, tagClass, emptyText) {
    if (!items || items.length === 0) {
        return `<span class="card-empty">${emptyText}</span>`;
    }

    const tags = items
        .map(function (item) {
            return `<span class="tag ${tagClass}">${item}</span>`;
        })
        .join("");

    return `<div class="tag-list">${tags}</div>`;
}


// =============================================
// SECTION 5: AI EXPLANATION CARD RENDERER
// Builds the premium AI card HTML.
// The explanation text is initially empty —
// typewriterEffect() fills it in after the card
// is inserted into the DOM.
//
// aiText: the string from data.ai_explanation
//         (may be null/undefined/empty)
// =============================================

function renderAICard(aiText) {
    // Normalise: treat null / undefined / blank as "no explanation"
    const hasText = aiText && aiText.trim().length > 0;

    return `
        <!--
            AI EXPLANATION CARD
            The outer div (.card-ai-wrapper) creates the
            animated gradient border via its background +
            the 1.5px padding gap trick.
            The inner div (.card-ai) is the actual content.
        -->
        <div class="card-ai-wrapper">
            <div class="card-ai">

                <!-- Header row: icon · title/subtitle · badges · [i] -->
                <div class="card-ai-header">

                    <!-- Robot emoji with CSS glow filter -->
                    <div class="ai-icon">🤖</div>

                    <!-- Title + subtitle -->
                    <div class="ai-title-block">
                        <div class="ai-title">AI Explanation</div>
                        <div class="ai-subtitle">
                            Generated from: Dictionary + FAISS + Graph Context
                        </div>
                    </div>

                    <!-- Badge cluster — Gemini pulses to draw the eye -->
                    <div class="ai-badges">
                        <span class="algo-badge badge-gemini badge-gemini-pulse">
                            Gemini 2.5 Flash
                        </span>
                        <span class="algo-badge badge-gen-ai">
                            Generative AI
                        </span>
                        <!--
                            Info button — opens the Gemini modal.
                            Uses the same openModal() system as all other cards.
                        -->
                        <button
                            class="info-btn"
                            onclick="openModal('ai_explanation')"
                            title="How Gemini AI Explanation works"
                        >i</button>
                    </div>

                </div>

                <!--
                    Mini pipeline inside the AI card.
                    Shows the RAG flow visually so visitors
                    instantly understand the data provenance.
                -->
                <div class="ai-mini-pipeline">
                    <span class="ai-pipe-step ai-pipe-dict">📚 Dictionary</span>
                    <span class="ai-pipe-arrow">→</span>
                    <span class="ai-pipe-step ai-pipe-faiss">🔷 FAISS Embeddings</span>
                    <span class="ai-pipe-arrow">→</span>
                    <span class="ai-pipe-step ai-pipe-graph">🕸️ Graph BFS</span>
                    <span class="ai-pipe-arrow">→</span>
                    <span class="ai-pipe-step ai-pipe-gem">✦ Gemini 2.5 Flash</span>
                    <span class="ai-pipe-arrow">→</span>
                    <span class="ai-pipe-step ai-pipe-out">💬 Explanation</span>
                </div>

                <!-- Thin gradient divider between pipeline and text -->
                <div class="ai-divider"></div>

                <!--
                    The explanation text area.
                    id="ai-explanation-text" is used by typewriterEffect()
                    to find this element after the card is in the DOM.
                    .typewriter-cursor adds the blinking ▌ via CSS ::after.
                -->
                <div
                    id="ai-explanation-text"
                    class="ai-explanation-text ${hasText ? 'typewriter-cursor' : ''}"
                >${hasText ? '' : '<span class="card-empty">No AI explanation available.</span>'}</div>

            </div>
        </div>
    `;
}


// =============================================
// SECTION 6: TYPEWRITER EFFECT
// Animates text character-by-character into
// the element with id="ai-explanation-text".
//
// Called AFTER renderResults() puts the card
// into the DOM (because the element must exist).
//
// text:  the full explanation string
// speed: milliseconds per character (default 18ms)
//        18ms ≈ 55 chars/sec — fast but readable
// =============================================

function typewriterEffect(text, speed) {
    speed = speed || 18;

    const el = document.getElementById("ai-explanation-text");

    // Safety: element must exist and text must be non-empty
    if (!el || !text || text.trim().length === 0) return;

    // Ensure the blinking cursor class is present while typing
    el.classList.add("typewriter-cursor");

    let index = 0;      // current character position
    el.textContent = ""; // start blank

    // Use setInterval to add one character at a time
    const interval = setInterval(function () {
        // Append the next character
        el.textContent += text[index];
        index++;

        // When all characters have been written, stop the interval
        // and remove the cursor class (stops the blinking cursor)
        if (index >= text.length) {
            clearInterval(interval);
            el.classList.remove("typewriter-cursor");
        }
    }, speed);
}


// =============================================
// SECTION 7: CARD HEADER BUILDER
// Generates the header row for each result card:
//   [Section Label]  [Algorithm Badge]  [i button]
//
// algoKey: key into ALGO_INFO (e.g. "semantic")
// =============================================

function renderCardHeader(sectionLabel, algoKey) {
    const info = ALGO_INFO[algoKey];

    // If no info entry exists for this key, render a plain label
    if (!info) {
        return `<div class="card-header">
            <span class="card-label">${sectionLabel}</span>
        </div>`;
    }

    return `
        <div class="card-header">
            <span class="card-label">${sectionLabel}</span>
            <span class="algo-badge ${info.badgeClass}">${info.label}</span>
            <button
                class="info-btn"
                onclick="openModal('${algoKey}')"
                title="How ${info.title} works"
            >i</button>
        </div>
    `;
}


// =============================================
// SECTION 8: RESULTS RENDERER
// Builds the full results HTML from the API data.
// Order: AI Explanation first, then all other cards.
// Each card has: header (with badge + info btn) + body.
// =============================================

function renderResults(data) {
    const dict = data.dictionary || {};

    // Extract the AI explanation — may be null/undefined from backend
    const aiExplanation = data.ai_explanation || "";

    const html = `

        <!-- Word title -->
        <div class="result-header">
            <div class="result-word">${data.query}<span>.</span></div>
        </div>

        <!-- Responsive card grid -->
        <div class="cards-grid">

            <!--
                AI EXPLANATION CARD — always first, full width.
                renderAICard() builds the HTML; typewriterEffect()
                is called separately after this HTML is in the DOM.
            -->
            ${renderAICard(aiExplanation)}

            <!-- DEFINITION — full width -->
            <div class="card card-wide">
                ${renderCardHeader("Definition", "definition")}
                <div class="card-body">
                    ${dict.definition || '<span class="card-empty">No definition found.</span>'}
                </div>
            </div>

            <!-- SYNONYMS -->
            <div class="card">
                ${renderCardHeader("Synonyms", "synonyms")}
                <div class="card-body">
                    ${renderTags(dict.synonyms, "tag", "No synonyms found.")}
                </div>
            </div>

            <!-- ANTONYMS -->
            <div class="card">
                ${renderCardHeader("Antonyms", "antonyms")}
                <div class="card-body">
                    ${renderTags(dict.antonyms, "tag-neutral", "No antonyms found.")}
                </div>
            </div>

            <!-- FAISS SEMANTIC SEARCH -->
            <div class="card">
                ${renderCardHeader("Semantic Search", "semantic")}
                <div class="card-body">
                    ${renderTags(data.semantic, "tag", "No semantic matches.")}
                </div>
            </div>

            <!-- GRAPH BFS RESULTS -->
            <div class="card">
                ${renderCardHeader("Graph Results", "graph")}
                <div class="card-body">
                    ${renderTags(data.graph, "tag", "No graph results.")}
                </div>
            </div>

            <!-- TRIE AUTOCOMPLETE -->
            <div class="card">
                ${renderCardHeader("Autocomplete", "autocomplete")}
                <div class="card-body">
                    ${renderTags(data.autocomplete, "tag", "No autocomplete suggestions.")}
                </div>
            </div>

            <!-- LEVENSHTEIN FUZZY MATCHES -->
            <div class="card">
                ${renderCardHeader("Fuzzy Matches", "fuzzy")}
                <div class="card-body">
                    ${renderTags(data.fuzzy, "tag", "No fuzzy matches.")}
                </div>
            </div>

        </div>
    `;

    return html;
}


// =============================================
// SECTION 9: INFO MODAL — OPEN / CLOSE
// openModal(algoKey) — builds modal HTML from
//   ALGO_INFO and shows the overlay.
// closeModal()       — hides the overlay.
// =============================================

function openModal(algoKey) {
    const info = ALGO_INFO[algoKey];
    if (!info) return;

    // Build the pipeline steps HTML
    const pipelineHTML = info.pipeline
        .map(function (step, index) {
            const arrow = index < info.pipeline.length - 1
                ? `<div class="modal-pipe-arrow">↓</div>`
                : "";
            return `<div class="modal-pipe-step">${step}</div>${arrow}`;
        })
        .join("");

    // Inject HTML into the modal content area
    document.getElementById("modal-content").innerHTML = `
        <div class="modal-title">${info.title}</div>
        <div class="modal-badge">
            <span class="algo-badge ${info.badgeClass}">${info.label}</span>
        </div>

        <div class="modal-section-label">Purpose</div>
        <p class="modal-text">${info.purpose}</p>

        <div class="modal-section-label">Time Complexity</div>
        <div class="complexity-chip">${info.complexity}</div>

        <div class="modal-section-label">Pipeline</div>
        <div class="modal-pipeline">${pipelineHTML}</div>

        <div class="modal-section-label">Note</div>
        <p class="modal-text">${info.note}</p>
    `;

    // Show the overlay
    document.getElementById("modal-overlay").classList.add("visible");

    // Prevent page scroll while modal is open
    document.body.style.overflow = "hidden";
}

function closeModal() {
    document.getElementById("modal-overlay").classList.remove("visible");
    document.body.style.overflow = "";
}

// Close modal with Escape key
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeModal();
    }
});


// =============================================
// SECTION 10: ARCHITECTURE PANEL TOGGLE
// Toggles the collapsible "How This Search Works"
// panel by setting max-height dynamically.
// (CSS transition animates the height change.)
// =============================================

function toggleArchPanel() {
    const panel  = document.getElementById("arch-panel");
    const body   = document.getElementById("arch-body");
    const toggle = panel.querySelector(".arch-toggle");

    const isOpen = panel.classList.contains("open");

    if (isOpen) {
        // Collapse: set explicit height then animate to 0
        body.style.maxHeight = body.scrollHeight + "px";
        // Force reflow before changing (needed for the CSS transition to fire)
        body.offsetHeight;
        body.style.maxHeight = "0";
        panel.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
    } else {
        // Expand: animate to the full scroll height
        body.style.maxHeight = body.scrollHeight + "px";
        panel.classList.add("open");
        toggle.setAttribute("aria-expanded", "true");
    }
}


// =============================================
// SECTION 11: MAIN SEARCH FUNCTION
// Called when user clicks Search or presses Enter.
// Steps:
//   1. Read query from input
//   2. Hide empty state, clear results, show loader
//   3. Fetch from FastAPI backend
//   4. Parse and render result cards
//   5. Kick off typewriter animation for AI card
//   6. Handle errors gracefully
// =============================================

async function searchWord() {
    const query = document.getElementById("query").value.trim();

    // Don't search if empty
    if (!query) return;

    // Reset UI
    document.getElementById("results").innerHTML = "";
    setError(false);
    setLoading(true);
    hideEmptyState();

    try {
        // Call the FastAPI backend
        const response = await fetch(
            `http://127.0.0.1:8000/search?query=${encodeURIComponent(query)}`
        );

        // Surface HTTP errors
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Render all result cards into the DOM.
        // The AI card HTML is included but its text area is empty.
        document.getElementById("results").innerHTML = renderResults(data);

        /*
          Kick off the typewriter animation AFTER innerHTML is set.
          This is important — typewriterEffect() looks for
          #ai-explanation-text in the DOM, so it must exist first.

          We use a tiny setTimeout(0) to yield to the browser's
          render cycle, ensuring the new DOM nodes are fully painted
          before we start writing characters.
        */
        const aiText = data.ai_explanation || "";
        if (aiText.trim().length > 0) {
            setTimeout(function () {
                typewriterEffect(aiText, 18);
            }, 0);
        }

    } catch (error) {
        // Backend unreachable or returned an error
        console.error("Search failed:", error);
        setError(true);

    } finally {
        // Always hide loader
        setLoading(false);
    }
}