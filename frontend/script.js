// async function searchWord() {

//     const query =
//         document.getElementById(
//             "query"
//         ).value;

//     const response =
//         await fetch(
//             `http://127.0.0.1:8000/search?query=${query}`
//         );

//     const data =
//         await response.json();

//     document.getElementById(
//         "results"
//     ).innerHTML = `

//         <div class="section">
//             <h2>${data.query}</h2>
//             <p>
//                 ${data.dictionary?.definition || "No definition"}
//             </p>
//         </div>

//         <div class="section">
//             <h3>Synonyms</h3>
//             <p>
//                 ${data.dictionary?.synonyms?.join(", ") || "None"}
//             </p>
//         </div>

//         <div class="section">
//             <h3>Antonyms</h3>
//             <p>
//                 ${data.dictionary?.antonyms?.join(", ") || "None"}
//             </p>
//         </div>

//         <div class="section">
//             <h3>Semantic Search</h3>
//             <p>
//                 ${data.semantic.join(", ")}
//             </p>
//         </div>

//         <div class="section">
//             <h3>Graph Results</h3>
//             <p>
//                 ${data.graph.join(", ")}
//             </p>
//         </div>

//         <div class="section">
//             <h3>Autocomplete</h3>
//             <p>
//                 ${data.autocomplete.join(", ")}
//             </p>
//         </div>

//         <div class="section">
//             <h3>Fuzzy Matches</h3>
//             <p>
//                 ${data.fuzzy.join(", ")}
//             </p>
//         </div>

//     `;
// }

// =============================================
// script.js — Semantic Dictionary AI
// Handles: search, API call, rendering results
// =============================================


// =============================================
// SECTION 1: KEYBOARD SHORTCUT
// Let the user press Enter to search,
// instead of having to click the button.
// =============================================

document.getElementById("query").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        searchWord();
    }
});


// =============================================
// SECTION 2: UI STATE HELPERS
// Small functions to show/hide loading spinner
// and the error message. Keeps the main function clean.
// =============================================

// Show or hide the loading spinner
function setLoading(isLoading) {
    const loader = document.getElementById("loading");
    if (isLoading) {
        loader.classList.remove("hidden");
    } else {
        loader.classList.add("hidden");
    }
}

// Show or hide the error message
function setError(hasError) {
    const errorBox = document.getElementById("error-message");
    if (hasError) {
        errorBox.classList.remove("hidden");
    } else {
        errorBox.classList.add("hidden");
    }
}


// =============================================
// SECTION 3: TAG LIST RENDERER
// Takes an array of strings and returns HTML
// for a row of pill-shaped tags.
//
// tagClass: "tag" for accent tags (synonyms, semantic)
//           "tag-neutral" for muted tags (antonyms)
// emptyText: what to show if the array is empty
// =============================================

function renderTags(items, tagClass, emptyText) {
    // If no items, show the fallback message
    if (!items || items.length === 0) {
        return `<span class="card-empty">${emptyText}</span>`;
    }

    // Build a pill for each item and join them
    const tags = items
        .map(function (item) {
            return `<span class="tag ${tagClass}">${item}</span>`;
        })
        .join("");

    return `<div class="tag-list">${tags}</div>`;
}


// =============================================
// SECTION 4: RESULTS RENDERER
// Takes the API response object and builds
// the full HTML for the results section.
// Each card is a separate visual block.
// =============================================

function renderResults(data) {
    // Safely extract dictionary data (it may be null/undefined)
    const dict = data.dictionary || {};

    // Build each card's HTML string
    const html = `

        <!-- Word title at the top -->
        <div class="result-header">
            <div class="result-word">${data.query}<span>.</span></div>
        </div>

        <!-- 2-column responsive grid of cards -->
        <div class="cards-grid">

            <!-- Definition card — spans full width -->
            <div class="card card-wide">
                <div class="card-label">Definition</div>
                <div class="card-body">
                    ${dict.definition || '<span class="card-empty">No definition found.</span>'}
                </div>
            </div>

            <!-- Synonyms -->
            <div class="card">
                <div class="card-label">Synonyms</div>
                <div class="card-body">
                    ${renderTags(dict.synonyms, "tag", "No synonyms found.")}
                </div>
            </div>

            <!-- Antonyms — uses neutral tag style -->
            <div class="card">
                <div class="card-label">Antonyms</div>
                <div class="card-body">
                    ${renderTags(dict.antonyms, "tag-neutral", "No antonyms found.")}
                </div>
            </div>

            <!-- FAISS semantic search results -->
            <div class="card">
                <div class="card-label">Semantic Search</div>
                <div class="card-body">
                    ${renderTags(data.semantic, "tag", "No semantic matches.")}
                </div>
            </div>

            <!-- Graph traversal results -->
            <div class="card">
                <div class="card-label">Graph Results</div>
                <div class="card-body">
                    ${renderTags(data.graph, "tag", "No graph results.")}
                </div>
            </div>

            <!-- Trie autocomplete suggestions -->
            <div class="card">
                <div class="card-label">Autocomplete</div>
                <div class="card-body">
                    ${renderTags(data.autocomplete, "tag", "No autocomplete suggestions.")}
                </div>
            </div>

            <!-- Levenshtein fuzzy matches -->
            <div class="card">
                <div class="card-label">Fuzzy Matches</div>
                <div class="card-body">
                    ${renderTags(data.fuzzy, "tag", "No fuzzy matches.")}
                </div>
            </div>

        </div>
    `;

    return html;
}


// =============================================
// SECTION 5: MAIN SEARCH FUNCTION
// Called when user clicks "Search" or presses Enter.
// Steps:
//   1. Read the query from the input
//   2. Show loading, clear old results
//   3. Call the FastAPI backend
//   4. Parse the response and render cards
//   5. Handle errors gracefully
// =============================================

async function searchWord() {
    // Read user input and trim whitespace
    const query = document.getElementById("query").value.trim();

    // Don't search if the input is empty
    if (!query) return;

    // Clear previous results and errors, show loader
    document.getElementById("results").innerHTML = "";
    setError(false);
    setLoading(true);

    try {
        // Call the FastAPI backend
        // Using template literal to insert the query into the URL
        const response = await fetch(
            `http://127.0.0.1:8000/search?query=${encodeURIComponent(query)}`
        );

        // If server returned an error status (e.g. 500), throw manually
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        // Parse the JSON body
        const data = await response.json();

        // Render the result cards into the DOM
        document.getElementById("results").innerHTML = renderResults(data);

    } catch (error) {
        // Something went wrong — show error state
        // (Most likely: backend is not running)
        console.error("Search failed:", error);
        setError(true);

    } finally {
        // Always hide the loader, whether search succeeded or failed
        setLoading(false);
    }
}