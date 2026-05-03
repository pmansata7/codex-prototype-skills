# Example SPEC.md - Cover Letter Tone Analyzer

This is a completed example spec for a simple prototype idea. Use it as a structural reference when generating specs for new ideas. Match the format, the level of detail in descriptions, and especially the style of binary success criteria.

---

# Cover Letter Tone Analyzer

> Paste a job description and cover letter, then get structured feedback on tone alignment, weak spots, and rewrite suggestions.

## Idea

**What:** A tool that analyzes whether a cover letter's tone matches what a job description signals the employer is looking for. It produces a structured scorecard with flagged sections and rewrite suggestions.
**Who:** Job seekers refining their cover letters before submission, especially people applying to multiple roles and adapting tone each time.
**Core interaction:** The user pastes a job description and a cover letter into a form, clicks `Analyze`, and receives a streamed structured result.

## AI Pattern

**Primary:** structured-generation
**Secondary:** none

## Work Packages

### WP-1: Project scaffolding
**Priority:** P0
**Dependencies:** none
**Description:** Create the Next.js project with AI SDK, a default AI Gateway model, and the minimal UI needed for a structured-generation starter. Set up the shared layout, styles, and environment variables so the project can build and run.

**Success criteria:**
- [ ] `npm run build` in the project root exits with code 0
- [ ] The file `.env.local` exists and contains `AI_GATEWAY_API_KEY=`
- [ ] The files `src/app/layout.tsx` and `src/app/globals.css` exist

### WP-2: Analysis schema and API route
**Priority:** P0
**Dependencies:** WP-1
**Description:** Define the Zod schema for the analysis output in a shared location. Create a `streamText` route at `/api/analyze` that uses `Output.object()` to stream a JSON object that matches the schema.

**Success criteria:**
- [ ] The file `src/lib/schemas/analysis.ts` exists and exports a Zod schema with top-level fields `scores`, `flaggedSections`, `rewriteSuggestions`, and `overallAssessment`
- [ ] The file `src/app/api/analyze/route.ts` exists and exports `POST`
- [ ] `POST /api/analyze` with body `{"prompt":"test"}` returns status 200

### WP-3: Input form UI
**Priority:** P0
**Dependencies:** WP-1
**Description:** Create the main page with two text areas, a submit button, and a results area. The page should read like an analysis tool, not a chat interface.

**Success criteria:**
- [ ] The page at `/` renders two text areas and a submit button
- [ ] The submit button is disabled when either required input is empty
- [ ] The page source includes labels or placeholders for both `job description` and `cover letter`

### WP-4: Wire analysis to UI
**Priority:** P0
**Dependencies:** WP-2, WP-3
**Description:** Connect the form to `/api/analyze` using `experimental_useObject`. Render partial structured results as they stream in from the server.

**Success criteria:**
- [ ] Submitting the form with valid input triggers a POST to `/api/analyze`
- [ ] The frontend imports `experimental_useObject as useObject` from `@ai-sdk/react`
- [ ] The frontend imports the shared schema from `src/lib/schemas/analysis.ts`

### WP-5: Scorecard display
**Priority:** P1
**Dependencies:** WP-4
**Description:** Replace raw output with a structured scorecard. Render scores, flagged sections, and rewrite suggestions from the schema fields.

**Success criteria:**
- [ ] Each score dimension renders with a label and numeric value
- [ ] Flagged sections render both `originalText` and `issue`
- [ ] Rewrite suggestions render both `original` and `suggested`

### WP-6: Validation and error handling
**Priority:** P1
**Dependencies:** WP-4
**Description:** Handle API errors and invalid submissions with explicit inline feedback. Reject submissions that are too short before making the API request.

**Success criteria:**
- [ ] Submitting with fewer than 20 characters in either field renders a validation message without sending a network request
- [ ] A non-200 API response renders an inline error state on the page
- [ ] The error state includes a retry action that re-submits the previous valid request

## Dependency Graph

```text
WP-1 (scaffold)
  |- WP-2 (schema + API)
  |- WP-3 (input form UI)
WP-2 + WP-3
  -> WP-4 (wire up)
WP-4
  |- WP-5 (scorecard display)
  |- WP-6 (validation + error handling)
```

WP-2 and WP-3 can execute in parallel.
WP-5 and WP-6 can execute in parallel after WP-4.

## Notes

- The schema design is the key implementation decision. Keep it stable and shared between backend and frontend.
- The route should use `streamText` with `Output.object()` so the client can consume the JSON stream with `experimental_useObject`.
- A sample-input helper can be added later as a P2 enhancement rather than part of the initial spec.
