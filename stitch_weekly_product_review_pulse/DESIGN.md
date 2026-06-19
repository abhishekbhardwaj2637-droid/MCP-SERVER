---
name: Pulse
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#bbcabf'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#86948a'
  outline-variant: '#3c4a42'
  surface-tint: '#4edea3'
  primary: '#4edea3'
  on-primary: '#003824'
  primary-container: '#10b981'
  on-primary-container: '#00422b'
  inverse-primary: '#006c49'
  secondary: '#bcc7de'
  on-secondary: '#263143'
  secondary-container: '#3e495d'
  on-secondary-container: '#aeb9d0'
  tertiary: '#ffb95f'
  on-tertiary: '#472a00'
  tertiary-container: '#e29100'
  on-tertiary-container: '#523200'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6ffbbe'
  primary-fixed-dim: '#4edea3'
  on-primary-fixed: '#002113'
  on-primary-fixed-variant: '#005236'
  secondary-fixed: '#d8e3fb'
  secondary-fixed-dim: '#bcc7de'
  on-secondary-fixed: '#111c2d'
  on-secondary-fixed-variant: '#3c475a'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  headline-xl:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1440px
  gutter: 24px
  margin-desktop: 40px
  margin-mobile: 16px
  unit-xs: 4px
  unit-sm: 8px
  unit-md: 16px
  unit-lg: 24px
  unit-xl: 48px
---

## Brand & Style
The design system is centered on a high-fidelity, premium aesthetic that blends **Glassmorphism** with a **Deep Slate Dark Mode**. It targets sophisticated users in fintech, SaaS, or data analytics who require a sense of precision and "active" monitoring.

The brand personality is technical yet approachable, characterized by "Emerald Glows" that signify growth and vitality against a calm, deep-sea background. The emotional response should be one of confidence, clarity, and futurism. We achieve this through translucent layering, vibrant accent highlights, and a structured layout that feels both lightweight and powerful.

## Colors
The palette is built on a foundation of **Deep Slate (#0F172A)** to provide maximum contrast for data visualization. 

- **Primary (Emerald Green):** Used exclusively for growth indicators, primary actions, and "active" state glows.
- **Surface (Glassy Slate):** All containers use a semi-transparent slate with a `backdrop-filter: blur(12px)`.
- **Accents:** Amber is reserved strictly for warnings or "cautionary" data points to ensure it doesn't compete with the Emerald primary.
- **Gradients:** Use a subtle radial gradient of Emerald (#10B981 at 15% opacity) behind key cards to create depth without clutter.

## Typography
This design system utilizes a dual-font strategy. **Outfit** provides a geometric, modern flair for headings, emphasizing the premium nature of the dashboard. **Inter** is used for all functional data, body text, and UI labels to ensure maximum legibility and a systematic, technical feel.

For data-heavy tables, use `body-sm` with a tabular-nums feature enabled. Headlines should always use tighter letter spacing to maintain a "locked-in" professional appearance.

## Layout & Spacing
The layout follows a **Fluid Grid** model with a maximum width of 1440px for content. We utilize a 12-column system on desktop and a 4-column system on mobile.

- **Desktop:** 24px gutters with 40px outer margins.
- **Tablet:** 16px gutters with 24px outer margins.
- **Mobile:** 16px gutters and margins.

Spacing follows an 8px base grid. Glassy cards should have a standard padding of `unit-lg` (24px) to allow the content to "breathe" against the background blur.

## Elevation & Depth
Depth is conveyed through **Glassmorphism** rather than traditional heavy shadows.
- **Level 1 (Base):** Deep Slate background (#0F172A).
- **Level 2 (Cards):** Surface Slate (#1E293B) at 70% opacity with a 12px backdrop blur and a 1px solid border at 10% white opacity.
- **Level 3 (Modals/Popovers):** Surface Slate at 90% opacity with a soft Emerald-tinted shadow (`0px 20px 40px rgba(0, 0, 0, 0.4)`).

Active elements (selected tabs, primary buttons) utilize an **Emerald Glow**—a soft outer glow using the primary color at 20% opacity to simulate an "on" state.

## Shapes
The design system uses a **Rounded** aesthetic to soften the technical nature of the dashboard.
- **Standard Cards/Inputs:** 0.5rem (8px) radius.
- **Main Containers:** 1rem (16px) radius.
- **Interactive Elements:** Buttons and tags use a slightly more pronounced rounding to feel "touchable."
- **Focus Rings:** Use a 2px offset Emerald border for keyboard navigation.

## Components

### Buttons
- **Primary:** Solid Emerald (#10B981) with white text. High-shine hover state.
- **Secondary:** Glassy Slate background with a 1px border.
- **Ghost:** No background, Emerald text, 8px roundedness.

### Input Fields
Inputs are semi-transparent with a 1px Slate border. On focus, the border transitions to Emerald and gains a 4px soft Emerald outer glow. Labels use `label-sm` positioned above the field.

### Glass Cards
The signature component. Must include:
1. `backdrop-filter: blur(12px)`
2. `background: rgba(30, 41, 59, 0.7)`
3. `border: 1px solid rgba(255, 255, 255, 0.1)`
4. Inner top-left highlight (1px white at 5% opacity).

### Chips & Tags
Small, highly rounded (pill) elements. For "Success" or "Growth" states, use a subtle Emerald background (10% opacity) with solid Emerald text.

### Data Charts
Line charts should use the Primary Emerald Green with a gradient area fill (Emerald to transparent). Grid lines in charts must be extremely subtle (rgba white at 5%).