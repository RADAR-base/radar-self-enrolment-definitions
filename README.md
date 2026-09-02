# radar-self-enrolment-definitions
Definition files to define the contents and behaviour of various parts of self enrolment portal such as study information, eligibility, consent and more.

The definitions are used by the self enrolment portal to render the [UI](https://github.com/RADAR-base/radar-self-enrolment-ui) and validate the user input. The definitions are written in JSON format and are loaded by the portal at runtime.


## protocol.json


## landingpage.json

# Landing Page JSON Configuration Guide

This document describes the structure and available block types for the `landingpage.json` file used to configure study landing pages.

## File Structure

The `landingpage.json` file should be placed at:
```
public/study/{studyId}/landingpage.json
```

The file has the following top-level structure:

```json
{
  "blocks": [
    // Array of block objects
  ]
}
```

## Common Block Properties

All blocks support the following common properties:

- **`blockType`** (required): The type of block. Must be one of: `hero`, `markdown`, `text`, `video`, `carousel`, `column`, `accordion`, `imageGallery`
- **`noCard`** (optional, boolean): If `true`, the block is rendered without a card wrapper. Default: `false`
- **`blockBackground`** (optional, string): CSS background value (color, gradient, image URL, etc.)
- **`blockPadding`** (optional, number | object): Padding value or responsive padding object
- **`sx`** (optional, object): Material-UI `sx` prop for custom styling
- **`title`** (optional, string | object): Block title. Can be a string or an object with `children` and `sx` properties
- **`subtitle`** (optional, string): Block subtitle

## Block Types

### 1. Hero Block (`blockType: "hero"`)

A large banner section typically used at the top of a landing page.

**Properties:**
- `blockType`: `"hero"` (required)
- `title`: string | object (optional)
  - If object: `{ children: string, sx?: object }`
- `subtitle`: string (optional) - Supports markdown
- `heroImage`: object (optional)
  - `src`: string - Image source path
  - `altText`: string - Alt text for the image
- `cta`: object (optional) - Primary call-to-action button
  - `text`: string - Button text
  - `href`: string - Link URL (relative paths are automatically prefixed with study ID)
  - `onClick`: function (optional) - Click handler
- `cta2`: object (optional) - Secondary call-to-action button
  - Same structure as `cta`

**Example:**
```json
{
  "blockType": "hero",
  "noCard": true,
  "blockBackground": "linear-gradient(to bottom left, rgba(0, 18, 24, 0.2), rgba(0, 18, 24, 0.7)), right / cover no-repeat url('/study/paprka/resources/knee.png'), #002e3d",
  "title": {
    "children": "PAPrKA: How active are people after knee replacement surgery?",
    "sx": {"color": "white"}
  },
  "subtitle": "The **P**hysical **A**ctivity **P**atterns after **K**nee **A**rthroplasty study...",
  "cta": {
    "text": "FAQs",
    "href": "paprka/faqs"
  },
  "cta2": {
    "text": "Join Study",
    "href": "paprka/enrol"
  }
}
```

---

### 2. Markdown Block (`blockType: "markdown"`)

Renders markdown content with optional title and subtitle.

**Properties:**
- `blockType`: `"markdown"` (required)
- `title`: string (optional)
- `subtitle`: string (optional)
- `content`: string (required) - Markdown content

**Example:**
```json
{
  "blockType": "markdown",
  "noCard": true,
  "title": "About the study",
  "blockBackground": "white",
  "content": "We are inviting people who had a knee replacement...\n\n<ol><li>Information you provide in a survey.</li></ol>"
}
```

---

### 3. Text Block (`blockType: "text"`)

Renders plain text content (no markdown parsing).

**Properties:**
- `blockType`: `"text"` (required)
- `title`: string (optional)
- `subtitle`: string (optional)
- `content`: string (required) - Plain text content

**Example:**
```json
{
  "blockType": "text",
  "title": "Study Information",
  "content": "This is plain text content without markdown formatting."
}
```

---

### 4. Video Block (`blockType: "video"`)

Embeds a video, either from YouTube or a direct video file.

**Properties:**
- `blockType`: `"video"` (required)
- `title`: string (optional)
- `subtitle`: string (optional)
- `video`: object (required) - Video configuration
  - **For YouTube videos:**
    - `youtubeId`: string - YouTube video ID
  - **For direct video files:**
    - `src`: string - Video file path
    - `type`: string - MIME type (e.g., "video/mp4")
    - `width`: number | string (optional)
    - `height`: number | string (optional)
    - `params`: object (optional) - Additional video element attributes

**Example (YouTube):**
```json
{
  "blockType": "video",
  "noCard": true,
  "blockBackground": "white",
  "video": {
    "youtubeId": "5mFgOzLI5ZM"
  }
}
```

**Example (Direct video):**
```json
{
  "blockType": "video",
  "video": {
    "src": "/study/paprka/videos/intro.mp4",
    "type": "video/mp4",
    "width": 800,
    "height": 450
  }
}
```

---

### 5. Carousel Block (`blockType: "carousel"`)

Displays a swipeable carousel of items, typically used for team member profiles or featured content.

**Properties:**
- `blockType`: `"carousel"` (required)
- `title`: string (optional)
- `subtitle`: string (optional)
- `items`: array (required) - Array of carousel items
  - `imgSrc`: string - Image source path
  - `title`: string (optional) - Item title
  - `content`: string (optional) - Item description
  - `href`: string (optional) - Link URL

**Example:**
```json
{
  "blockType": "carousel",
  "noCard": true,
  "title": "Meet The Team",
  "items": [
    {
      "imgSrc": "/study/paprka/resources/landingpage/profiles/will_dixon.png",
      "title": "Will Dixon",
      "content": "Professor of Digital Epidemiology",
      "href": "https://research.manchester.ac.uk/en/persons/will.dixon"
    }
  ]
}
```

---

### 6. Column Block (`blockType: "column"`)

A container that displays multiple child blocks side-by-side in columns.

**Properties:**
- `blockType`: `"column"` (required)
- `title`: string (optional)
- `subtitle`: string (optional)
- `sx`: object (optional) - Material-UI sx prop
- `content`: array | object (required) - Child blocks
  - Can be an array of block objects
  - Or an object with named block properties (e.g., `{ "block1": {...}, "block2": {...} }`)
  - Child blocks can be: `markdown`, `hero`, or `video` blocks

**Example:**
```json
{
  "blockType": "column",
  "noCard": true,
  "blockBackground": "white",
  "title": "",
  "content": [
    {
      "blockType": "markdown",
      "title": "Who can take part?",
      "content": "You must answer yes to all 5 questions..."
    },
    {
      "blockType": "markdown",
      "title": "What will I have to do?",
      "content": "1. Check you can take part in the study.\n2. Sign an electronic consent form."
    }
  ]
}
```

**Example (object format):**
```json
{
  "blockType": "column",
  "content": {
    "block1": {
      "blockType": "hero",
      "title": "Join the RADAR Project",
      "subtitle": "This is the default study landing page.",
      "cta": {
        "text": "Join Study",
        "href": "enrol"
      }
    },
    "block2": {
      "blockType": "markdown",
      "content": ""
    }
  }
}
```

---

### 7. Accordion Block (`blockType: "accordion"`)

Displays collapsible accordion items.

**Properties:**
- `blockType`: `"accordion"` (required)
- `title`: string (optional)
- `subtitle`: string (optional)
- `items`: array (required) - Array of accordion items
  - `title`: string - Accordion item title
  - `content`: string - Accordion item content (supports markdown)

**Example:**
```json
{
  "blockType": "accordion",
  "title": "Frequently Asked Questions",
  "items": [
    {
      "title": "What is the study about?",
      "content": "This study aims to..."
    },
    {
      "title": "How long does it take?",
      "content": "The study takes approximately..."
    }
  ]
}
```

---

### 8. Image Gallery Block (`blockType: "imageGallery"`)

Displays a responsive grid of images.

**Properties:**
- `blockType`: `"imageGallery"` (required)
- `title`: string | object (optional) - Can be a string or object with `children` and `sx`
- `images`: array (required) - Array of image objects
  - `src`: string - Image source path
  - `alt`: string - Alt text
  - `href`: string (optional) - Link URL when clicking the image
  - `caption`: string (optional) - Caption displayed over the image
- `columns`: number | object (optional) - Number of columns
  - Default: `{ xs: 1, sm: 2, md: 3, lg: 4 }`
  - Can be a number (applies to all breakpoints) or responsive object:
    - `xs`: number - Extra small screens
    - `sm`: number - Small screens
    - `md`: number - Medium screens
    - `lg`: number - Large screens
    - `xl`: number - Extra large screens
- `rows`: number | object (optional) - Limit number of rows (shows all images if not specified)
- `objectFit`: string (optional) - CSS object-fit value
  - Options: `"fill"`, `"contain"`, `"cover"`, `"none"`, `"scale-down"`
  - Default: `"cover"`
- `gap`: number (optional) - Spacing between images (theme spacing units)
  - Default: `2`
- `aspectRatio`: string (optional) - CSS aspect-ratio value
  - Default: `"1 / 1"`
- `borderRadius`: number | string (optional) - Border radius value
  - Default: `2`

**Example:**
```json
{
  "blockType": "imageGallery",
  "columns": {"xs": 1, "sm": 2, "md": 3, "lg": 3, "xl": 3},
  "gap": 1,
  "borderRadius": 0,
  "aspectRatio": "32/27",
  "objectFit": "fill",
  "images": [
    {
      "src": "/study/paprka/resources/landingpage/image_guide_overview/overview-guide-1.jpeg",
      "alt": "Step 1"
    },
    {
      "src": "/study/paprka/resources/landingpage/image_guide_overview/overview-guide-2.jpeg",
      "alt": "Step 2",
      "href": "/study/paprka/guide",
      "caption": "Guide Step 2"
    }
  ]
}
```

---

## Complete Example

Here's a complete example of a `landingpage.json` file:

```json
{
  "blocks": [
    {
      "blockType": "hero",
      "noCard": true,
      "blockBackground": "#002e3d",
      "title": "Welcome to Our Study",
      "subtitle": "Join us in advancing medical research.",
      "cta": {
        "text": "Join Study",
        "href": "enrol"
      }
    },
    {
      "blockType": "markdown",
      "noCard": true,
      "title": "About the Study",
      "content": "This study aims to collect important health data..."
    },
    {
      "blockType": "column",
      "noCard": true,
      "content": [
        {
          "blockType": "markdown",
          "title": "Eligibility",
          "content": "You must be 18 years or older..."
        },
        {
          "blockType": "markdown",
          "title": "What to Expect",
          "content": "The study involves..."
        }
      ]
    },
    {
      "blockType": "imageGallery",
      "title": "Study Process",
      "columns": {"xs": 2, "sm": 3, "md": 4},
      "images": [
        {"src": "/study/example/step1.jpg", "alt": "Step 1"},
        {"src": "/study/example/step2.jpg", "alt": "Step 2"}
      ]
    }
  ]
}
```

## Notes

- **Relative URLs**: Relative URLs in `href` properties are automatically prefixed with the study ID. For example, `"href": "enrol"` becomes `"/{studyId}/enrol"`.
- **External URLs**: URLs starting with a protocol (e.g., `http://`, `https://`, `mailto:`) are used as-is.
- **Markdown Support**: The `markdown` block type and `subtitle` fields in hero blocks support markdown formatting, including HTML.
- **Responsive Design**: Many properties support responsive values using breakpoint objects (`xs`, `sm`, `md`, `lg`, `xl`).
- **Styling**: Use `sx` properties for Material-UI styling and `blockBackground` for CSS backgrounds (colors, gradients, images).


## Scripts

The `scripts` directory contains scripts to pull definitions from external systems such as REDCap or local CSV files.

