# Globals CSS Template

Create `src/app/globals.css`.

If `create-next-app` or AI Elements already generated compatible base styles, keep those and remove only the demo-specific styles.

```css
@import "tailwindcss";

@plugin "tailwindcss-animate";

@custom-variant dark (&:is(.dark *));
```

Keep any existing shadcn-generated `@theme` blocks or CSS variables if they are already present.
