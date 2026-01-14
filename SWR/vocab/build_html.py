import json
import os
import base64

json_file = "all_curriculum.json"
output_html = "vocab_dashboard.html"

# CSS & JS content
css_content = """

    body {
        font-family: 'Outfit', sans-serif;
        margin: 0;
        padding: 20px;
        background-color: #fdfbf7;
        color: #333;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        min-height: 80vh;
        transition: max-width 0.3s ease;
    }
    .container.full-width {
        max-width: 95vw;
    }
    .container.bookmark-width {
        max-width: 950px;
    }
    h1, h2 {
        text-align: center;
        color: #333;
        margin: 0;
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        gap: 20px;
    }
    .logo {
        height: 60px;
        width: auto;
    }
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }
    .card {
        background: #fff;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        cursor: pointer;
        transition: transform 0.1s, box-shadow 0.1s;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 80px;
        font-weight: bold;
        color: #444;
        position: relative;
        overflow: hidden;
    }
    .card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #FF9A9E 0%, #FECFEF 99%, #FECFEF 100%);
        transform: scaleX(0);
        transform-origin: bottom right;
        transition: transform 0.3s ease-out;
    }
    .card:hover::after {
        transform: scaleX(1);
        transform-origin: bottom left;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        background-color: #f9f9f9;
        color: #000;
    }
    .card:active {
        transform: translateY(0);
    }
    
    /* Tools Card Specifics */
    .card.tools-card {
        color: #444;
        border: 2px solid #81E6D9; /* Green accent border */
        background-color: #f0fdf9; /* Very subtle green tint */
    }
    .card.tools-card::after {
        background: linear-gradient(90deg, #4FD1C5 0%, #38B2AC 100%);
    }
    .card.tools-card .icon-cog {
        fill: #38B2AC; /* Green accent icon */
    }
    .icon-cog {
        width: 24px;
        height: 24px;
        margin-right: 10px;
        fill: currentColor;
    }
    .btn-back {
        display: inline-block;
        padding: 8px 16px;
        background-color: #eee;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        margin-bottom: 20px;
        font-size: 14px;
    }
    .btn-back:hover {
        background-color: #ddd;
    }
    .list-item {
        padding: 20px;
        border-bottom: 1px solid #e0e0e0;
        cursor: pointer;
        font-size: 2rem;
        transition: background-color 0.2s;
    }
    .list-item:hover {
        background-color: #f0ebe4;
    }
    .big-word-view {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 70vh;
        text-align: center;
        width: 100%;
    }
    .big-word {
        font-weight: 700;
        color: #222;
        margin-bottom: 20px;
        line-height: 1.1;
        white-space: nowrap;
    }
    .hidden {
        display: none;
    }
    .year-section {
        margin-top: 20px;
    }
    .year-header {
        background: #eee;
        padding: 10px;
        border-radius: 4px;
        margin-bottom: 10px;
    }

    /* A4 Simulation on Screen */
    .a4-page {
        width: auto;
        min-width: 210mm;
        min-height: 297mm;
        padding: 15mm;
        margin: 20px auto;
        background: white;
        box-shadow: 0 0 15px rgba(0,0,0,0.15);
        box-sizing: border-box;
        position: relative;
        display: inline-block; /* Allow container to grow with content */
    }
    .container {
        text-align: center; /* Center the inline-block a4-page */
    }

    /* Print Styles */
    @media print {
        @page { 
            size: A4 portrait; 
            margin: 15mm; /* Apply margins to every page (top, bottom, left, right) */
        }
        body { 
            background: white !important; 
            padding: 0 !important;
        }
        .container { 
            box-shadow: none !important; 
            width: 100% !important; 
            max-width: none !important; 
            padding: 0 !important;
            margin: 0 !important;
            min-height: auto !important;
            background: none !important;
        }
        .a4-page {
            margin: 0 !important;
            box-shadow: none !important;
            width: 100% !important;
            min-height: auto !important;
            padding: 0 !important; /* Remove padding as @page handles margins now */
        }
        .btn-back, .header-container, .big-word-view, .grid, .list-item, #back-btn, .no-print, .vocab-header { 
            display: none !important; 
        }
        /* Only show the print containers */
        .print-container, .subject-print-container { 
            display: block !important; 
        }
    }

    .print-container {
        display: none; /* Hidden on screen normally */
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(2, auto); /* Explicit rows */
        gap: 3mm;
        justify-content: center;
        padding: 0;
        margin: 0 auto;
        width: 100%;
        page-break-inside: avoid;
    }

    .bookmark-cell {
        border: 2px solid #333; /* Solid rectangle */
        width: 42mm; /* Reduced width to fit 4 cols */
        height: 130mm;
        padding: 5px;
        display: flex;
        flex-direction: column;
        align-items: center;
        background: white;
        text-align: center;
        overflow: hidden;
        margin: 0 auto;
        break-inside: avoid;
    }

    .bookmark-title {
        font-weight: bold;
        font-size: 14pt;
        margin-bottom: 10px;
        border-bottom: 2px solid #333;
        width: 100%;
        padding-bottom: 5px;
        text-transform: uppercase;
    }

    .bookmark-list {
        font-size: 11pt;
        list-style: none;
        padding: 0;
        text-align: left;
        width: 100%;
    }
    
    .bookmark-list li {
        margin-bottom: 6px;
        line-height: 1.2;
        border-bottom: 1px dotted #ccc;
    }

    /* Screen preview for print view */
    .print-preview-mode .print-container {
        display: grid;
    }
    .print-preview-mode .header-container, 
    .print-preview-mode .grid, 
    .print-preview-mode .year-section {
        display: none;
    }
    
    .icon-bookmark {
        width: 24px;
        height: 24px;
        cursor: pointer;
        fill: #4FD1C5;
        transition: transform 0.2s;
    }
    .icon-bookmark:hover {
        transform: scale(1.1);
        fill: #38B2AC;
    }
    
    .vocab-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .vocab-toolbar {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    .subject-print-container {
        column-count: 3;
        column-gap: 15px;
        text-align: left;
    }
    .subject-print-item {
        break-inside: avoid;
        margin-bottom: 10px;
    }
    .subject-print-item h3 {
        background-color: #f4f4f4;
        padding: 4px 8px;
        border-left: 3px solid #333;
        border-radius: 0 4px 4px 0;
        margin-top: 0;
        margin-bottom: 5px;
        break-after: avoid;
        page-break-after: avoid;
        font-size: 11pt;
    }
    .subject-print-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 15px;
    }
    /* Print adjustments for subject view */
    @media print {
        .year-print-columns {
            column-count: 4 !important;
        }
    }
    .action-icon {
        width: 32px;
        height: 32px;
        cursor: pointer;
        stroke: #444;
        stroke-width: 1.5;
        fill: none;
        transition: stroke 0.2s, transform 0.2s;
    }
    .action-icon:hover {
        stroke: #000;
        transform: scale(1.1);
    }
    .subject-icon {
        width: 40px;
        height: 40px;
        margin-top: 10px;
        stroke: #aaa; /* Subtle grey */
        stroke-width: 1.5;
        fill: none;
    }
    .card:hover .subject-icon {
        stroke: #666; /* Darker on hover */
    }
"""

js_content = """
    // State
    let currentView = 'subjects';
    let selectedSubject = null;
    let selectedTopic = null;
    let selectedWord = null;
    
    // Elements
    const container = document.getElementById('app-content');
    const backBtn = document.getElementById('back-btn');
    const title = document.getElementById('page-title');
    const mainHeader = document.querySelector('.header-container');

    function getSubjectIcon(subject) {
        const s = subject.toLowerCase();
        let path = '';
        
        // Default (Book/Generic)
        path = '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/> <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>';

        if (s.includes('math')) { // Calculator/Maths
             path = '<rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="16" y1="14" x2="16" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/>';
        } else if (s.includes('science') || s.includes('physics') || s.includes('biology') || s.includes('chem')) { // Flask
            path = '<path d="M10 2v7.31"/><path d="M14 2v7.31"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/>';
        } else if (s.includes('art') || s.includes('design')) { // Palette / Pen
            path = '<circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/>';
        } else if (s.includes('history')) { // Clock/Time
             path = '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>';
        } else if (s.includes('geography')) { // Globe
             path = '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>';
        } else if (s.includes('computing') || s.includes('computer')) { // Monitor
             path = '<rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>';
        } else if (s.includes('music')) { // Music Note
             path = '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>';
        } else if (s.includes('drama')) { // Masks (Smile)
             path = '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/>';
        } else if (s.includes('pe') || s.includes('physical')) { // Activity
             path = '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>';
        } else if (s.includes('english')) { // Feather/Book
             path = '<path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5z"/><line x1="16" y1="8" x2="2" y2="22"/><line x1="17.5" y1="15" x2="9" y2="15"/>';
        } else if (s.includes('french') || s.includes('spanish') || s.includes('language')) { // Message bubble
             path = '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>';
        } else if (s.includes('re') || s.includes('religious')) { // Peace/Dove simplified
            path = '<path d="M4.5 12h15"/><path d="M12 4.5v15"/><circle cx="12" cy="12" r="10"/>'; // Cross for now as generic RE symbol or generic spiritual
        }

        return `<svg class="subject-icon" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">${path}</svg>`;
    }

    function render() {
        container.innerHTML = '';
        backBtn.classList.add('hidden');
        title.textContent = 'Curriculum Vocabulary';
        title.style.display = 'block'; // Ensure visible by default
        
        // Reset container width unless in specific views
        const cont = document.querySelector('.container');
        cont.classList.remove('full-width');
        cont.classList.remove('bookmark-width');
        
        // Default: Show main header
        if (mainHeader) mainHeader.style.display = 'flex';

        if (currentView === 'subjects') {
            renderSubjects();
        } else if (currentView === 'topics') {
            backBtn.classList.remove('hidden');
            // Hide main header for inline custom look
            if (mainHeader) mainHeader.style.display = 'none';
            renderTopics();
        } else if (currentView === 'vocab') {
            backBtn.classList.remove('hidden');
            // We usually hide title in renderVocab anyway, let's keep consistent
            if (mainHeader) mainHeader.style.display = 'none'; 
            renderVocab();
        } else if (currentView === 'word') {
            backBtn.classList.remove('hidden');
            title.textContent = '';
            document.querySelector('.container').classList.add('full-width');
            renderWord();
        } else if (currentView === 'tools') {
            backBtn.classList.remove('hidden');
            title.textContent = 'Tools';
            renderTools();
        } else if (currentView === 'print-bookmarks') {
            backBtn.classList.remove('hidden');
            if (mainHeader) mainHeader.style.display = 'none';
            title.textContent = 'Printable Bookmarks';
            // Allow container to fit A4 page naturally
            document.querySelector('.container').classList.add('full-width'); 
            renderBookmarks();
        } else if (currentView === 'print-subject-vocab') {
            backBtn.classList.remove('hidden');
            if (mainHeader) mainHeader.style.display = 'none';
            title.textContent = selectedSubject.Subject + ' Vocabulary';
            document.querySelector('.container').classList.add('full-width'); 
            renderSubjectPrint();
        }
    }

    function renderSubjects() {
        const grid = document.createElement('div');
        grid.className = 'grid';
        
        // Sort subjects alphabetically
        const subjects = Object.values(curriculumData).sort((a,b) => a.Subject.localeCompare(b.Subject));
        
        subjects.forEach(sub => {
            const card = document.createElement('div');
            card.className = 'card';
            
            // Flex column for content
            card.style.flexDirection = 'column';
            card.style.justifyContent = 'center';

            card.innerHTML = `<span>${sub.Subject}</span>` + getSubjectIcon(sub.Subject);
            
            card.onclick = () => {
                selectedSubject = sub;
                currentView = 'topics';
                render();
            };
            grid.appendChild(card);
        });

        // Add Tools Card
        const toolsCard = document.createElement('div');
        toolsCard.className = 'card tools-card';
        // Cog SVG
        const cogSvg = '<svg class="icon-cog" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>';
        
        toolsCard.innerHTML = cogSvg + "Tools";
        toolsCard.onclick = () => {
            currentView = 'tools';
            render();
        };
        grid.appendChild(toolsCard);

        container.appendChild(grid);
    }

    function renderTopics() {
        // Custom Header for Subject View: INLINE [Logo] [Title] [Icon]
        const headerDiv = document.createElement('div');
        headerDiv.className = 'vocab-header';
        headerDiv.style.display = 'flex';
        headerDiv.style.alignItems = 'center';
        headerDiv.style.justifyContent = 'center';
        headerDiv.style.gap = '20px';
        
        // 1. Logo
        const logo = document.createElement('img');
        logo.src = logoSrc; // Global variable injected by Python
        logo.style.height = '60px';
        logo.style.width = 'auto';
        
        // 2. Title
        const titleEl = document.createElement('h2');
        titleEl.textContent = selectedSubject.Subject;
        titleEl.style.margin = '0';
        titleEl.style.fontSize = '2.5rem'; // Make it nice and big

        // 3. Subject Icon
        const iconDiv = document.createElement('div');
        iconDiv.innerHTML = getSubjectIcon(selectedSubject.Subject);
        // Make icon slightly larger to match text
        const svg = iconDiv.querySelector('svg');
        if (svg) {
            svg.style.width = '50px';
            svg.style.height = '50px';
            svg.style.marginTop = '0';
        }
        
        headerDiv.appendChild(logo);
        headerDiv.appendChild(titleEl);
        headerDiv.appendChild(iconDiv);
        
        // Container for everything
        const wrapper = document.createElement('div');
        wrapper.appendChild(headerDiv);

        // HR line
        const hr = document.createElement('hr');
        hr.style.margin = '15px auto';
        hr.style.width = '80%';
        hr.style.border = '0';
        hr.style.borderTop = '1px solid #ddd';
        
        wrapper.appendChild(hr);

        // Toolbar
        const toolbar = document.createElement('div');
        toolbar.className = 'vocab-toolbar';

        // List/Print Icon
        const listBtn = document.createElement('div');
        listBtn.innerHTML = '<svg class="action-icon" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>';
        listBtn.title = "Print Full Subject Vocabulary";
        listBtn.onclick = () => {
             currentView = 'print-subject-vocab';
             render();
        };

        toolbar.appendChild(listBtn);
        wrapper.appendChild(toolbar);
        
        container.appendChild(wrapper);

        // topics are grouped by year
        selectedSubject.Years.forEach(yearGroup => {
            const section = document.createElement('div');
            section.className = 'year-section';
            
            const header = document.createElement('h3');
            header.className = 'year-header';
            header.textContent = `Year ${yearGroup.Year}`;
            section.appendChild(header);

            const grid = document.createElement('div');
            grid.className = 'grid';

            yearGroup.Topics.forEach(topic => {
                // Skip empty topics
                if (!topic.Topic && (!topic.KeyVocab || topic.KeyVocab.length === 0)) return;
                
                const displayTitle = topic.Topic ? topic.Topic : "General/Untitled Topic";

                const card = document.createElement('div');
                card.className = 'card';
                card.textContent = displayTitle;
                card.onclick = () => {
                    selectedTopic = topic;
                    currentView = 'vocab';
                    render();
                };
                grid.appendChild(card);
            });
            section.appendChild(grid);
            container.appendChild(section);
        });
    }

    function renderVocab() {
        // Clear previous content
        container.innerHTML = '';
        
        const headerDiv = document.createElement('div');
        headerDiv.className = 'vocab-header';
        
        // Re-use logic: SWR Logo - Title
        // Actually for Topic view, just SWR (above? logic handled by hiding mainHeader)
        // User didn't specify topic page, but consistency implies we want SWR logo here too or re-enable mainHeader?
        // Let's re-enable standard look for Topic View (Logo above, Topic Title below) but hide main header implies we must rebuild it.
        // Or simpler: For now, just rebuild custom header with just SWR + Topic Title.
        
        const logo = document.createElement('img');
        logo.src = logoSrc;
        logo.style.height = '50px';
        logo.style.width = 'auto';
        logo.style.display = 'block';
        logo.style.margin = '0 auto 10px auto';
        
        const titleEl = document.createElement('h2');
        titleEl.textContent = selectedTopic.Topic || "Topic Vocabulary";
        titleEl.style.margin = '0';
        
        headerDiv.appendChild(logo);
        headerDiv.appendChild(titleEl);
        
        // HR line
        const hr = document.createElement('hr');
        hr.style.margin = '15px auto';
        hr.style.width = '80%';
        hr.style.border = '0';
        hr.style.borderTop = '1px solid #ddd';

        // Toolbar for icons
        const toolbar = document.createElement('div');
        toolbar.className = 'vocab-toolbar';

        // Bookmark Icon (Outline)
        const bookmarkBtn = document.createElement('div');
        bookmarkBtn.innerHTML = '<svg class="action-icon" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>';
        bookmarkBtn.title = "Create Printable Bookmarks";
        bookmarkBtn.onclick = () => {
             currentView = 'print-bookmarks';
             render();
        };

        toolbar.appendChild(bookmarkBtn);
        // Can append more icons here later

        headerDiv.appendChild(titleEl);
        headerDiv.appendChild(hr);
        headerDiv.appendChild(toolbar);
        
        container.appendChild(headerDiv);

        // Hide main page title in this view since we have custom header
        title.style.display = 'none';

        const list = document.createElement('div');
        
        if (selectedTopic.KeyVocab && selectedTopic.KeyVocab.length > 0) {
            selectedTopic.KeyVocab.forEach(word => {
                const item = document.createElement('div');
                item.className = 'list-item';
                item.textContent = word;
                item.onclick = () => {
                    selectedWord = word;
                    currentView = 'word';
                    render();
                };
                list.appendChild(item);
            });
        } else {
            list.textContent = "No vocabulary words listed for this topic.";
            list.style.textAlign = 'center';
            list.style.color = '#777';
        }
        
        container.appendChild(list);
    }
    
    function renderBookmarks() {
        // Hide standard title
        title.style.display = 'block';
        
        // Print Button (Icon)
        const printBtn = document.createElement('div');
        printBtn.className = 'no-print';
        printBtn.style.textAlign = 'center';
        printBtn.style.marginBottom = '20px';
        printBtn.style.cursor = 'pointer';
        printBtn.title = "Print Bookmarks";
        printBtn.innerHTML = '<svg style="width:48px;height:48px;fill:#444;" viewBox="0 0 24 24"><path d="M19 8h-1V3H6v5H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zM8 5h8v3H8V5zm8 12v4H8v-4h8zm2-2v-2H6v2H4v-4c0-.55.45-1 1-1h14c.55 0 1 .45 1 1v4h-2z"/><circle cx="18" cy="11.5" r="1"/></svg>';
        
        printBtn.onclick = () => window.print();
        
        container.appendChild(printBtn);

        const grid = document.createElement('div');
        grid.className = 'print-container print-preview-mode';
        grid.style.display = 'grid'; // Ensure grid display

        // Create 8 identical bookmarks
        for (let i = 0; i < 8; i++) {
            const cell = document.createElement('div');
            cell.className = 'bookmark-cell';
            
            // Logo centered at top
            const logo = document.createElement('img');
            logo.src = logoSrc;
            logo.style.height = '30px'; 
            logo.style.width = 'auto';
            logo.style.marginTop = '0px';
            logo.style.marginBottom = '8px';
            
            const bTitle = document.createElement('div');
            bTitle.className = 'bookmark-title';
            bTitle.textContent = selectedTopic.Topic || selectedSubject.Subject;
            
            const ul = document.createElement('ul');
            ul.className = 'bookmark-list';
            
            if (selectedTopic.KeyVocab) {
                selectedTopic.KeyVocab.forEach(word => {
                    const li = document.createElement('li');
                    li.textContent = word;
                    ul.appendChild(li);
                });
            }
            
            // Subject Icon at bottom
            const footerIcon = document.createElement('div');
            footerIcon.style.marginTop = 'auto';
            footerIcon.style.paddingTop = '10px';
            footerIcon.innerHTML = getSubjectIcon(selectedSubject.Subject);
            // Adjust icon size for bookmark if needed, though default 40px is likely fine
            
            cell.appendChild(logo);
            cell.appendChild(bTitle);
            cell.appendChild(ul);
            cell.appendChild(footerIcon);
            grid.appendChild(cell);
        }
        
        // Wrap in A4 page
        const page = document.createElement('div');
        page.className = 'a4-page';
        page.appendChild(grid);
        
        container.appendChild(printBtn);
        container.appendChild(page);
    }

    function renderWord() {
        const view = document.createElement('div');
        view.className = 'big-word-view';
        
        const wordEl = document.createElement('div');
        wordEl.className = 'big-word';
        wordEl.textContent = selectedWord;
        
        view.appendChild(wordEl);
        container.appendChild(view);
        
        // Fit text logic using binary search for performance
        const parent = view;
        const el = wordEl;
        let min = 10;
        let max = 600; // Cap max reasonable size
        let optimal = min;
        
        while (min <= max) {
            const mid = Math.floor((min + max) / 2);
            el.style.fontSize = mid + 'px';
            
            if (el.scrollWidth <= parent.clientWidth && el.scrollHeight <= parent.clientHeight) {
                optimal = mid;
                min = mid + 1;
            } else {
                max = mid - 1;
            }
        }
        el.style.fontSize = optimal + 'px';
        
        
        // Re-run on resize
        window.onresize = () => renderWord();
    }

    function renderSubjectPrint() {
        title.style.display = 'none';

        // Header
        const headerDiv = document.createElement('div');
        headerDiv.className = 'subject-print-header';
        
        // Print Button
        const printBtn = document.createElement('div');
        printBtn.className = 'no-print';
        printBtn.style.textAlign = 'center';
        printBtn.style.marginBottom = '20px';
        printBtn.style.cursor = 'pointer';
        printBtn.title = "Print List";
        printBtn.innerHTML = '<svg style="width:40px;height:40px;fill:#444;" viewBox="0 0 24 24"><path d="M19 8h-1V3H6v5H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zM8 5h8v3H8V5zm8 12v4H8v-4h8zm2-2v-2H6v2H4v-4c0-.55.45-1 1-1h14c.55 0 1 .45 1 1v4h-2z"/><circle cx="18" cy="11.5" r="1"/></svg>';
        printBtn.onclick = () => window.print();
        headerDiv.appendChild(printBtn);

        // Wrap in A4 page
        const page = document.createElement('div');
        page.className = 'a4-page';
        
        // Inline Header: Title + Icon
        const hTitle = document.createElement('h2');
        hTitle.textContent = selectedSubject.Subject + " Vocabulary";
        hTitle.style.marginBottom = '0';
        
        const hIcon = document.createElement('div');
        hIcon.innerHTML = getSubjectIcon(selectedSubject.Subject);
        
        headerDiv.innerHTML = '';
        headerDiv.appendChild(hTitle);
        headerDiv.appendChild(hIcon);
        
        page.appendChild(headerDiv);

        const wrapper = document.createElement('div');
        wrapper.className = 'subject-print-wrapper';
        wrapper.style.display = 'block';

        selectedSubject.Years.forEach(yearGroup => {
            // 1. Year Header (Full Width)
            const yearHeader = document.createElement('h3');
            yearHeader.textContent = `Year ${yearGroup.Year}`;
            yearHeader.className = 'year-print-header';
            yearHeader.style.backgroundColor = '#eee';
            yearHeader.style.borderLeft = '4px solid #333';
            yearHeader.style.padding = '6px 10px';
            yearHeader.style.marginBottom = '5px';
            yearHeader.style.marginTop = '10px';
            yearHeader.style.fontSize = '14pt'; 
            yearHeader.style.fontWeight = '700';
            yearHeader.style.color = '#000';
            yearHeader.style.pageBreakAfter = 'avoid';
            yearHeader.style.breakAfter = 'avoid';
            yearHeader.style.pageBreakInside = 'avoid';
            yearHeader.style.breakInside = 'avoid';
            
            // 2. Column Container for THIS Year
            const yearCols = document.createElement('div');
            yearCols.className = 'year-print-columns';
            // Inline styles for certainty
            yearCols.style.columnCount = '4';
            yearCols.style.columnGap = '15px';
            yearCols.style.marginBottom = '20px';
            yearCols.style.columnFill = 'balance'; /* Try to balance heights */
            
            // Add topics to this year's column container
            yearGroup.Topics.forEach(topic => {
                 if (!topic.KeyVocab || topic.KeyVocab.length === 0) return;
                 
                 const topicBlock = document.createElement('div');
                 topicBlock.className = 'subject-print-item';
                 // Allow topic to split across columns to better balance height
                 topicBlock.style.breakInside = 'auto'; 
                 
                 // Topic Title
                 const tTitle = document.createElement('h4');
                 tTitle.textContent = topic.Topic || "Untitled Topic";
                 tTitle.style.marginBottom = '5px';
                 tTitle.style.marginTop = '10px';
                 tTitle.style.fontSize = '9pt';
                 tTitle.style.color = '#222';
                 tTitle.style.breakAfter = 'avoid'; /* Keep title with list */
                 tTitle.style.pageBreakAfter = 'avoid';
                 
                 // List
                 const ul = document.createElement('ul');
                 ul.style.marginTop = '0';
                 ul.style.paddingLeft = '15px';
                 ul.style.fontSize = '8pt'; 
                 ul.style.marginBottom = '10px';
                 ul.style.textAlign = 'left'; /* Ensure left alignment */
                 
                 topic.KeyVocab.forEach(word => {
                     const li = document.createElement('li');
                     li.textContent = word;
                     li.style.marginBottom = '2px';
                     li.style.border = 'none'; 
                     ul.appendChild(li);
                 });
                 
                 topicBlock.appendChild(tTitle);
                 topicBlock.appendChild(ul);
                 yearCols.appendChild(topicBlock);
            });
            
            wrapper.appendChild(yearHeader);
            wrapper.appendChild(yearCols);
        });

        page.appendChild(wrapper);
        
        container.appendChild(printBtn); // Button outside/first
        container.appendChild(page);
    }

    function renderTools() {
        const msg = document.createElement('div');
        msg.innerHTML = '<p style="text-align:center; color:#666;">Tools page content comng soon...</p>';
        container.appendChild(msg);
    }

    backBtn.onclick = () => {
        if (currentView === 'topics') {
            currentView = 'subjects';
            selectedSubject = null;
        } else if (currentView === 'vocab') {
            currentView = 'topics';
            selectedTopic = null;
        } else if (currentView === 'word') {
            currentView = 'vocab';
            selectedWord = null;
        } else if (currentView === 'tools') {
            currentView = 'subjects';
        } else if (currentView === 'print-bookmarks') {
            currentView = 'vocab';
        } else if (currentView === 'print-subject-vocab') {
            currentView = 'topics';
        }
        render();
    };

    // Init
    render();
"""

try:
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = f.read()

    # Encode logo
    logo_path = "swr.png"
    logo_base64 = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo" alt="SWR Logo">' if logo_base64 else ''

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Curriculum Vocabulary</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
    {css_content}
    </style>
</head>
<body>
    <div class="container">
        <button id="back-btn" class="btn-back hidden">← Back</button>
        <div class="header-container">
            {logo_html}
            <h1 id="page-title">Curriculum Vocabulary</h1>
        </div>
        <div id="app-content"></div>
    </div>

    <script>
        const curriculumData = {json_data};
        const logoSrc = "data:image/png;base64,{logo_base64}";
        {js_content}
    </script>
</body>
</html>
"""

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Successfully generated {output_html}")
    
except Exception as e:
    print(f"Error generating HTML: {e}")
