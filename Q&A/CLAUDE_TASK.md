# Frontend Technical Specification: Rebranding to QSnera & Large-Format Marble Installation Section

## 1. Overview & Project Objectives
This specification outlines the technical requirements for rebranding the luxury stone website from **AURELIA** to **QSnera**, and adding a new high-impact interactive section showcasing the studio's elite capability in **Large-Format Marble Installation**.

The target file for implementation is [index.html](file:///Users/rodionyalanskiy/Desktop/premium-tiling-website/index.html). The layout must remain highly premium, utilizing the existing design system (CSS variables, fonts, margins, animations, and responsive practices).

---

## 2. Phase 1: Global Rebranding (Aurelia ➔ QSnera)
All references to the old company name "AURELIA" must be replaced with the new name "QSnera" (or "QSnera Studio" where appropriate). 

### 2.1 String Replacement Map
Update the following elements in [index.html](file:///Users/rodionyalanskiy/Desktop/premium-tiling-website/index.html):
- **Page Title (Line 7)**: 
  * Old: `<title>AURELIA | Luxury Tile &amp; Stone Installation Studio</title>`
  * New: `<title>QSnera | Luxury Tile &amp; Stone Installation Studio</title>`
- **Meta Description (Line 6)**:
  * Old: `content="AURELIA is a luxury tile and stone installation studio. We specialize in bespoke bookmatched marble slab fabrication..."`
  * New: `content="QSnera is a luxury tile and stone installation studio. We specialize in bespoke bookmatched marble slab fabrication..."`
- **Logo text (Line 212-221)**:
  * Update the text inside `.logo` from "AURELIA" to "QSnera".
- **Studio Introduction Paragraph (Line 1335)**:
  * Update "At Aurelia, we view..." to "At QSnera, we view..."
- **Testimonial References**:
  * Line 1594: Update "Aurelia's attention to detail..." to "QSnera's attention to detail..."
  * Line 1603: Update "...Aurelia's installation..." to "...QSnera's installation..."
  * Line 1612: Update "...Aurelia set them organically..." to "...QSnera set them organically..."
- **Contact Details (Lines 1544, 1657)**:
  * Update the email addresses from `inquire@aureliastone.com` to `inquire@qsnera.com`.
  * Update the street address (Line 1540) from `104 Aurelia Way, San Francisco, CA` to `104 QSnera Way, San Francisco, CA`.
- **Footer Copyright & Logo (Lines 1637, 1671)**:
  * Update the logo block and copyright text from "AURELIA Studio" to "QSnera Studio".

---

## 3. Phase 2: "Large-Format Marble Installation" Section
A new content section must be inserted directly between the **Philosophy** section (`#philosophy`, Line 1328) and the **Services** section (`#services`, Line 1345).

### 3.1 Layout & Visual Design
- **Section ID**: `marble-showcase`
- **Classes**: `marble-showcase reveal` (must utilize the `.reveal` class to integrate with the scroll-reveal observer script).
- **Background**: Use `--color-charcoal-mid` (`#161618`) to maintain the alternating light/dark background structure between sections.
- **Layout Structure**: 
  - Standard `.container` wrapper with a 2-column grid (`.marble-grid`) on desktop:
    - **Left Column**: Visual interactive panel (`.marble-visual-container`) representing a bookmatched marble slab wall.
    - **Right Column**: Detailed text copy (`.marble-content-container`) describing the engineering, handling, and bookmatching process.
  - Responsive collapse to 1 column at `max-width: 992px`.

### 3.2 Left Column: Interactive "Bookmatched Vein Alignment" Widget
To showcase "precision," the visual container should contain an interactive CSS/JS component simulating a bookmatched Calacatta marble wall. 
- **The Concept**: The visual displays two side-by-side slabs (meeting at a center grout line). By horizontal mirroring, a beautiful bookmatched pattern is formed.
- **Interactivity**: An overlay control toggle (e.g., button or switch) allows users to switch between **"Aligned (Premium)"** and **"Misaligned (Standard)"** vein states.
- **CSS Mirroring Trick**: Fulfill this using the existing asset `assets/hero-bg.png` or `assets/portfolio-1.png`. The left slab shows the normal image cropped; the right slab shows the same image flipped horizontally (`transform: scaleX(-1)`) to automatically create a symmetrical bookmatch pattern.
- **State Transition**: When the user clicks the toggle:
  - In **"Aligned"** state: The right slab aligns perfectly with the left slab's veins.
  - In **"Misaligned"** state: The right slab's background translates vertically (`transform: scaleX(-1) translateY(-60px)`) to simulate a poor installation with broken veins.

### 3.3 Right Column: Copy & Typography
- **Section Subtitle**: `<span class="section-subtitle">THE PINNACLE OF STONE ARTISTRY</span>`
- **Section Title**: `<h2 class="section-title">Large-Format Marble</h2>`
- **Paragraph 1**: 
  > "Installing massive natural stone slabs is a complex architectural discipline. We specialize in the handling, fabrication, and mounting of premium marble slabs—including Calacatta, Carrara, and Statuario—reaching heights of up to 10 feet with zero tolerance for error."
- **Paragraph 2**:
  > "Through custom bookmatching, we mirror the slab's organic veining across seams, transforming walls, wetrooms, and fireplaces into continuous, flowing works of art."
- **Specs Checklist**: An elegant `<ul>` list styled with gold markers (matching `.precision-spec-list`):
  * **Precision Bookmatching**: Exact symmetrical vein alignment across all horizontal and vertical seams.
  * **Sub-Millimeter Joints**: Hairline grout planes under 1mm filled with color-matched micro-epoxy resins.
  * **Structural Epoxy Anchoring**: Mechanical and chemical reinforcement engineered for heavy vertical wall claddings.
  * **Zero-Lippage Guarantee**: Strict flatness monitoring using mechanical tension systems.
- **Call To Action**:
  * An elegant `<a href="#portfolio" class="btn-gold">Explore Marble Projects</a>` button.

---

## 4. Technical Reference Snippets

### 4.1 HTML Structure
```html
<!-- ==========================================================================
     MARBLE SHOWCASE SECTION
     ========================================================================== -->
<section class="marble-showcase reveal" id="marble-showcase">
  <div class="container">
    <div class="marble-grid">
      
      <!-- Visual Column -->
      <div class="marble-visual-container">
        <div class="marble-slab-wall" id="marble-slab-wall">
          <div class="slab slab-left"></div>
          <div class="seam-line"><span class="seam-pulse"></span></div>
          <div class="slab slab-right"></div>
        </div>
        
        <!-- Toggle Control Overlay -->
        <div class="bookmatch-controls">
          <span class="control-label">Vein Match:</span>
          <button class="control-btn active" id="btn-align-yes">Aligned</button>
          <button class="control-btn" id="btn-align-no">Standard</button>
        </div>
      </div>
      
      <!-- Content Column -->
      <div class="marble-content-container">
        <span class="section-subtitle">The Pinnacle of Stone Artistry</span>
        <h2 class="section-title" style="margin-bottom: 2rem;">Large-Format Marble</h2>
        <p class="marble-desc" style="margin-bottom: 1.5rem;">
          Installing massive natural stone slabs is a complex architectural discipline. We specialize in the handling, fabrication, and mounting of premium marble slabs—including Calacatta, Carrara, and Statuario—reaching heights of up to 10 feet with zero tolerance for error.
        </p>
        <p class="marble-desc" style="margin-bottom: 2.5rem;">
          Through custom bookmatching, we mirror the slab's organic veining across seams, transforming walls, wetrooms, and fireplaces into continuous, flowing works of art.
        </p>
        
        <ul class="precision-spec-list" style="margin-bottom: 3rem;">
          <li><strong>Precision Bookmatching</strong>: Exact symmetrical vein alignment across all seams.</li>
          <li><strong>Sub-Millimeter Joints</strong>: Hairline grout planes under 1mm filled with color-matched micro-epoxy.</li>
          <li><strong>Structural Epoxy Anchoring</strong>: Mechanical and chemical reinforcement for heavy vertical walls.</li>
          <li><strong>Zero-Lippage Guarantee</strong>: Flatness monitoring using advanced tension systems.</li>
        </ul>
        
        <a href="#portfolio" class="btn-gold">Explore Marble Projects</a>
      </div>
      
    </div>
  </div>
</section>
```

### 4.2 CSS Guidelines
Insert this styling into the `<style>` block in `index.html`:
```css
/* ==========================================================================
   MARBLE SHOWCASE SECTION
   ========================================================================== */
.marble-showcase {
  padding: 10rem 0;
  background-color: var(--color-charcoal-mid);
  border-bottom: 1px solid var(--color-gold-border);
}

.marble-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6rem;
  align-items: center;
}

/* Bookmatched Visual Mockup */
.marble-visual-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
}

.marble-slab-wall {
  position: relative;
  display: flex;
  height: 450px;
  border: 1px solid var(--color-gold-border);
  overflow: hidden;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
}

.slab {
  width: 50%;
  height: 100%;
  background-image: url('assets/hero-bg.png'); /* Using hero-bg as marble texture placeholder */
  background-size: cover;
  transition: transform 0.8s cubic-bezier(0.16, 1, 0.3, 1), background-position 0.8s;
}

.slab-left {
  background-position: right center;
  border-right: none;
}

.slab-right {
  background-position: left center;
  transform: scaleX(-1); /* Flips texture to create mirroring */
}

/* Active misalignment state */
.marble-slab-wall.misaligned .slab-right {
  transform: scaleX(-1) translateY(-60px); /* Disrupts vein alignment */
}

/* Central Seam Joint */
.seam-line {
  position: absolute;
  top: 0;
  left: 50%;
  width: 1px;
  height: 100%;
  background-color: var(--color-gold-matte);
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

.seam-pulse {
  width: 8px;
  height: 8px;
  background-color: var(--color-gold-bright);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--color-gold-bright);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.6); opacity: 1; box-shadow: 0 0 15px var(--color-gold-bright); }
  100% { transform: scale(1); opacity: 0.8; }
}

/* Interactive Controls UI */
.bookmatch-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.control-label {
  font-size: 0.85rem;
  color: var(--color-gray-text);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.control-btn {
  background: transparent;
  border: 1px solid var(--color-gold-border);
  color: var(--color-gray-text);
  padding: 0.5rem 1.5rem;
  font-family: var(--font-sans);
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
  transition: var(--transition-fast);
}

.control-btn.active {
  border-color: var(--color-gold-matte);
  color: var(--color-gold-matte);
  background-color: rgba(197, 168, 128, 0.05);
}

.control-btn:hover {
  border-color: var(--color-gold-bright);
  color: var(--color-white);
}

.marble-desc {
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--color-gray-text);
  font-weight: 300;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .marble-grid {
    grid-template-columns: 1fr;
    gap: 4rem;
  }
  .marble-showcase {
    padding: 6rem 0;
  }
  .marble-slab-wall {
    height: 350px;
  }
}
```

### 4.3 JavaScript Controller Code
Add this block near the interactive script elements at the bottom of the page:
```javascript
    // ==========================================================================
    // MARBLE SHOWCASE - INTERACTIVE VEIN MATCHING TOGGLE
    // ==========================================================================
    const btnAlignYes = document.getElementById('btn-align-yes');
    const btnAlignNo = document.getElementById('btn-align-no');
    const slabWall = document.getElementById('marble-slab-wall');

    if (btnAlignYes && btnAlignNo && slabWall) {
      const setAlignment = (align) => {
        if (align) {
          slabWall.classList.remove('misaligned');
          btnAlignYes.classList.add('active');
          btnAlignNo.classList.remove('active');
        } else {
          slabWall.classList.add('misaligned');
          btnAlignYes.classList.remove('active');
          btnAlignNo.classList.add('active');
        }
      };

      btnAlignYes.addEventListener('click', () => setAlignment(true));
      btnAlignNo.addEventListener('click', () => setAlignment(false));
    }
```

---

## 5. Acceptance & Verification Criteria
1. **Responsive Validation**: Section must collapse smoothly into a single-column layout at viewport widths below `992px`. The marble wall should preserve a consistent aspect ratio or height.
2. **Animation Integration**: Section must correctly trigger the `.reveal` transition animation when scrolled into view.
3. **No External Dependencies**: The bookmatch mirroring effect must utilize existing assets (`assets/hero-bg.png`) via CSS `transform: scaleX(-1)` and coordinate offset shifting, keeping the project lightweight.
4. **Clean Code Integration**: Ensure all new CSS classes do not conflict with existing elements and use semantic layout naming. All console logs and temporary code must be omitted.
