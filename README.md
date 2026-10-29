# My Dashboard — React + Vite

A responsive business analytics dashboard for exploring e-commerce sales, marketplace fees, estimated profit, returns, channel performance, and basic data quality. Built with React, Vite, Recharts, and Lucide icons.

## Features
- Responsive KPI dashboard, monthly revenue trend, category mix, and channel comparison
- Searchable order explorer with CSV export
- Upload a CSV dataset directly in the browser
- Rule-based natural-language question interface (not yet connected to an LLM)
- Return reasons and basic data-quality checks
- Synthetic sample data and reset-to-demo option
- Vercel configuration for static Vite deployment

## Run locally
Requires Node.js 20+ recommended.

```bash
npm install
npm run dev
```

Build and preview:

```bash
npm run build
npm run preview
```

## Deploy to Vercel
Import this repository into Vercel, select **Vite**, use `npm run build` as the build command and `dist` as the output directory. The included `vercel.json` sets these values.

## CSV upload
Common columns supported include `order_id`/`id`, `order_date`/`date`, `gross_sales`/`sales`/`revenue`, `order_status`/`status`, `product_name`/`product`, `marketplace_fee`/`fee`, and `return_reason`/`reason`. Review imported values before interpreting results.

## Metric caveats
The included dataset is synthetic. Growth percentages are visual demo indicators, not actual period-over-period calculations. Return rate is returned rows divided by non-cancelled rows. Estimated profit is simplified demo data and is not suitable for financial decisions.

## Tech stack
React · Vite · Recharts · Lucide · CSS

## Portfolio summary
Built an interactive analytics interface to explore sales performance, category and channel mix, return reasons, marketplace fees, and data quality. Roadmap: validated data layer, real period comparisons, KPI tests, and secured AI-assisted analysis.
