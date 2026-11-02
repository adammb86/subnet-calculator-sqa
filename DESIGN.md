---
name: Clarity Workspace
colors:
  surface: '#f7fafd'
  surface-dim: '#d7dade'
  surface-bright: '#f7fafd'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4f7'
  surface-container: '#ebeef2'
  surface-container-high: '#e5e8ec'
  surface-container-highest: '#e0e3e6'
  on-surface: '#181c1f'
  on-surface-variant: '#414754'
  inverse-surface: '#2d3134'
  inverse-on-surface: '#eef1f5'
  outline: '#727785'
  outline-variant: '#c1c6d6'
  surface-tint: '#005bc0'
  primary: '#005bbf'
  on-primary: '#ffffff'
  primary-container: '#1a73e8'
  on-primary-container: '#ffffff'
  inverse-primary: '#adc7ff'
  secondary: '#5b5f64'
  on-secondary: '#ffffff'
  secondary-container: '#dde0e6'
  on-secondary-container: '#5f6368'
  tertiary: '#006d2a'
  on-tertiary: '#ffffff'
  tertiary-container: '#16893a'
  on-tertiary-container: '#000701'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc7ff'
  on-primary-fixed: '#001a41'
  on-primary-fixed-variant: '#004493'
  secondary-fixed: '#dfe3e8'
  secondary-fixed-dim: '#c3c7cc'
  on-secondary-fixed: '#181c20'
  on-secondary-fixed-variant: '#43474c'
  tertiary-fixed: '#8ffa9b'
  tertiary-fixed-dim: '#73dc82'
  on-tertiary-fixed: '#002108'
  on-tertiary-fixed-variant: '#00531e'
  background: '#f7fafd'
  on-background: '#181c1f'
  surface-variant: '#e0e3e6'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: '600'
    lineHeight: 3.5rem
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 2rem
    fontWeight: '500'
    lineHeight: 2.5rem
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: 2rem
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 1.375rem
    fontWeight: '500'
    lineHeight: 1.75rem
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: '500'
    lineHeight: 1.5rem
  body-lg:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.625rem
  body-md:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.375rem
  body-sm:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '400'
    lineHeight: 1.125rem
  label-md:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '500'
    lineHeight: 1.25rem
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '500'
    lineHeight: 1rem
    letterSpacing: 0.02em
  code-lg:
    fontFamily: JetBrains Mono
    fontSize: 1rem
    fontWeight: '500'
    lineHeight: 1.5rem
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 0.875rem
    fontWeight: '500'
    lineHeight: 1.25rem
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 0.75rem
    fontWeight: '400'
    lineHeight: 1rem
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 2rem
  margin-sm: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system embodies an approachable, utilitarian, and distraction-free learning ecosystem inspired by modern educational software and classic Google design language. It balances pristine clarity with structured technical rigor, catering to students, IT professionals, and educators studying networking, cloud systems, and computer science.

The visual ethos blends **Corporate Modern** with **Technical Minimalism**:
- **Pristine & Uncluttered:** Extensive breathing room, stark white backgrounds, and subdued tonal surfaces establish high focus and zero visual fatigue.
- **Analytical & Direct:** Crisp lines, legible typography, and dedicated monospaced treatments for technical data (IP addresses, CIDR notation, binary strings, and subnet masks).
- **Calm Authority:** A distinct, friendly blue focal accent guides user action without overwhelming the content, supported by universally understood semantic states.

## Colors

The palette relies on high-luminance canvas tones, meticulous neutral stepping, and targeted semantic accents:

### Surface & Foundation
- **Canvas / Base:** `#FFFFFF`
- **Surface Level 1 (Off-white / Canvas Background):** `#F8F9FA`
- **Surface Level 2 (Subtle Dividers / Inactive Fills):** `#F1F3F4`
- **Border Default:** `#DADCE0`
- **Border Subtle:** `#E8EAED`

### Typography & Neutrals
- **Text Primary:** `#202124` (High-contrast headlines and primary data values)
- **Text Body / Secondary:** `#3C4043` (Default body, primary readable content)
- **Text Muted:** `#5F6368` (Captions, labels, supporting metadata)
- **Text Tertiary / Placeholder:** `#70757A`

### Primary Interactive
- **Primary Base:** `#1A73E8`
- **Primary Hover:** `#174EA6`
- **Primary Active / Pressed:** `#1558D6`
- **Primary Container / Tint:** `#E8F0FE`
- **Primary Text on Accent:** `#FFFFFF`

### Semantic Alerts & Feedback
- **Success Base:** `#1E8E3E`
- **Success Container:** `#E6F4EA`
- **Success Text:** `#137333`
- **Error Base:** `#D93025`
- **Error Container:** `#FCE8E6`
- **Error Text:** `#C5221F`
- **Warning Base:** `#F9AB00`
- **Warning Container:** `#FEF7E0`
- **Warning Text:** `#B06000`

## Typography

The type hierarchy employs **Inter** for UI, narrative instruction, and headline structures, delivering neutral readability and rhythmic clarity. **JetBrains Mono** is reserved as a functional accent for all raw technical parameters: IP addresses, subnet masks, hexadecimal addresses, binary blocks, and CLI snippets.

- **Headlines:** Use moderate weights (`500` or `600`) to avoid visual heaviness while preserving clean structural hierarchy.
- **Body Text:** Renders in `#3C4043` for reduced glare across white surfaces during extended reading and study sessions.
- **Technical/Code Tokens:** Must always render in `JetBrains Mono` with subtle letter-spacing adjustments to preserve tabular alignment in mathematical and network calculators.

## Layout & Spacing

This design system uses an **8-point mathematical spacing system** overlaid onto a responsive grid:

- **Desktop (≥ 1280px):** 12-column layout with `2rem` (32px) margins and `1.5rem` (24px) gutters. Maximum content canvas spans 1280px centered.
- **Tablet (768px – 1279px):** 8-column layout with `1.5rem` (24px) margins and `1rem` (16px) gutters. Complex two-column comparison layouts reflow into stacked modules.
- **Mobile (< 768px):** 4-column layout with `1rem` (16px) margins and `1rem` (16px) gutters. Technical tables shift to horizontally scrollable modules or segmented cards.

Component layout relies strictly on atomic rhythm (`space-xs` through `space-xl`) to maintain consistent breathing space between labels, interactive fields, and container boundaries.

## Elevation & Depth

Depth is established primarily through **tonal layers and subtle, low-opacity ambient drop shadows**, avoiding harsh structural borders:

- **Base Layer (Flat):** `0 0 0 0 transparent`. Sits directly on `#F8F9FA` or `#FFFFFF`, demarcated with a 1px border of `#DADCE0`.
- **Level 1 (Default Cards & Modules):** `0 1px 2px 0 rgba(60, 64, 67, 0.30), 0 1px 3px 1px rgba(60, 64, 67, 0.15)`. Used for resting module cards, tool panels, and interactive question blocks.
- **Level 2 (Hover & Active Elements):** `0 1px 3px 0 rgba(60, 64, 67, 0.30), 0 4px 8px 3px rgba(60, 64, 67, 0.15)`. Used when hovering actionable cards or dragging network nodes.
- **Level 3 (Dropdowns & Popovers):** `0 4px 6px 0 rgba(60, 64, 67, 0.30), 0 8px 12px 6px rgba(60, 64, 67, 0.15)`. Applied to autocomplete menus, dropdown selectors, and context popovers.
- **Level 4 (Modals & Dialogs):** `0 8px 10px 1px rgba(60, 64, 67, 0.20), 0 16px 24px 2px rgba(60, 64, 67, 0.14)`. Reserved for modal confirmation alerts and network topology wizards.

## Shapes

The geometric framework follows a layered curvature system that maintains soft, approachable edges without feeling overly playful:

- **Interactive Elements (Buttons, Form Inputs, Dropdowns):** `8px` (`0.5rem`) for a clean, sturdy feel.
- **Cards, Modules, and Display Panels:** `12px` to `16px` (`0.75rem` to `1rem`), creating clear boundary definitions for learning tasks.
- **Badges, Tags, and Pill Counters:** Fully rounded (`9999px`) to distinguish categorical metadata from actionable rectangular triggers.

## Components

### Buttons
- **Primary Button:** `#1A73E8` solid background, `#FFFFFF` text, 8px radius, 36px/40px height, 16px horizontal padding. Hover shifts to `#174EA6`; active to `#1558D6`.
- **Secondary / Tonal Button:** `#E8F0FE` background, `#1A73E8` text, 8px radius. Hover shifts to `#D2E3FC`.
- **Outlined Button:** `#FFFFFF` background, 1px solid `#DADCE0`, `#1A73E8` or `#3C4043` text. Hover shifts to `#F8F9FA` with border tint `#DADCE0`.
- **Text Button:** Transparent background, `#1A73E8` text, 8px radius. Hover renders `#F8F9FA` background fill.

### Inputs & Selectors
- **Text Inputs:** 40px height, `#FFFFFF` fill, 1px solid `#DADCE0`, 8px radius, 12px horizontal padding.
- **Focus State:** 2px solid `#1A73E8` outline with 0px offset.
- **Error State:** 2px solid `#D93025` border, accompanied by `#D93025` error helper text and `#FCE8E6` inline alert indicators.
- **Monospaced Input Fields (IP, CIDR):** Pre-styled with `JetBrains Mono` text, tabular number alignment, and light gray placeholder `#70757A`.

### Cards & Learning Containers
- **Default Card:** `#FFFFFF` background, 1px solid `#DADCE0`, 12px or 16px border-radius, Level 1 shadow.
- **Interactive Exercise Card:** Hover elevates to Level 2 shadow with border shifting subtly to `#1A73E8`.
- **Inspection Well / Inset Panel:** `#F8F9FA` or `#F1F3F4` fill, 8px radius, no shadow, inset 1px border `#E8EAED` (ideal for CIDR breakdown tables and routing tables).

### Badges & Status Chips
- **Neutral / Informational Chip:** `#F1F3F4` fill, `#3C4043` text, 9999px radius, 8px horizontal padding, 24px height.
- **Success Status Badge:** `#E6F4EA` fill, `#137333` text, `label-sm` weight, with optional 6px emerald dot indicator.
- **Error Status Badge:** `#FCE8E6` fill, `#C5221F` text, `label-sm` weight.
- **Active Focus Chip:** `#E8F0FE` fill, `#1A73E8` text, 1px solid `#1A73E8`.

### Checkboxes & Radios
- **Unchecked:** 18px box/circle, 2px solid `#5F6368`, transparent background.
- **Checked:** `#1A73E8` fill, white checkmark or center circle, smooth scale transition.
- **Focus Ring:** 4px radial wash of `#E8F0FE`.

### Specialized Educational Modules
- **Subnet / Binary Visualizer Block:** Multi-segment pill display using alternating `#F8F9FA` and `#FFFFFF` cells with `JetBrains Mono`, featuring active boundary split lines rendered in `#1A73E8`.
- **Step-by-Step Progress Rail:** 4px connecting track in `#DADCE0`, active segments filled with `#1A73E8`, and completed nodes highlighted with `#1E8E3E`.