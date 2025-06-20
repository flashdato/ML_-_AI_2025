document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const recommendBtn = document.getElementById('recommend-btn');
    const movieInput = document.getElementById('movie-input');
    const autocompleteResults = document.getElementById('autocomplete-results');
    const recommendationsGrid = document.getElementById('recommendations-grid');
    const errorMessage = document.getElementById('error-message');
    const loader = document.getElementById('loader');

    // --- API Endpoints ---
    const RECOMMEND_API_URL = 'http://127.0.0.1:5001/recommend';
    const MOVIES_API_URL = 'http://127.0.0.1:5001/movies';

    // --- State ---
    let allMovieTitles = [];

    // --- Functions ---

    // Fetch all movie titles when the page loads
    async function fetchMovieTitles() {
        try {
            const response = await fetch(MOVIES_API_URL);
            if (!response.ok) throw new Error('Could not fetch movie list.');
            const data = await response.json();
            allMovieTitles = data.movie_titles || [];
        } catch (error) {
            console.error("Error fetching movie titles:", error);
            showError("Could not load movie suggestions. Please try refreshing.");
        }
    }

    // Main function to get recommendations
    async function handleRecommendation() {
        const movieTitle = movieInput.value.trim();
        
        if (movieTitle === "") {
            showError("Please select a movie from the list.");
            return;
        }

        clearResults();
        showLoader(true);

        try {
            const response = await fetch(RECOMMEND_API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ movie_title: movieTitle }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Could not fetch recommendations.');
            }

            const data = await response.json();
            displayRecommendations(data.recommendations);
        } catch (error) {
            showError(`Error: ${error.message}`);
        } finally {
            showLoader(false);
        }
    }

    // Handle user typing in the input field
    function handleAutocomplete() {
        const query = movieInput.value.toLowerCase();
        closeAllLists();
        if (!query) return;

        let suggestions = allMovieTitles
            .filter(title => title.toLowerCase().includes(query))
            .slice(0, 7); // Show max 7 suggestions

        suggestions.forEach(title => {
            const suggestionDiv = document.createElement('div');
            // Bold the matching part of the text
            const regex = new RegExp(query, 'gi');
            suggestionDiv.innerHTML = title.replace(regex, (match) => `<strong>${match}</strong>`);
            
            suggestionDiv.addEventListener('click', () => {
                movieInput.value = title;
                closeAllLists();
            });
            autocompleteResults.appendChild(suggestionDiv);
        });
    }

    // Display the recommended movies in a grid
    function displayRecommendations(movies) {
        if (!movies || movies.length === 0) {
            showError("No recommendations found for this movie.");
            return;
        }
        movies.forEach(movie => {
            const card = document.createElement('div');
            card.className = 'movie-card';
            card.textContent = movie;
            recommendationsGrid.appendChild(card);
        });
    }

    // Helper functions for UI
    function showLoader(show) {
        loader.style.display = show ? 'block' : 'none';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }

    function clearResults() {
        recommendationsGrid.innerHTML = '';
        errorMessage.textContent = '';
        errorMessage.style.display = 'none';
    }

    function closeAllLists() {
        autocompleteResults.innerHTML = '';
    }

    // --- Event Listeners ---
    recommendBtn.addEventListener('click', handleRecommendation);
    movieInput.addEventListener('input', handleAutocomplete);

    // Close the autocomplete list if user clicks elsewhere
    document.addEventListener('click', (e) => {
        if (e.target !== movieInput) {
            closeAllLists();
        }
    });

    // --- Initial Load ---
    fetchMovieTitles();
});