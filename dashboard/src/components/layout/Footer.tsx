export function Footer() {
  return (
    <footer className="mt-auto border-t border-border/40 py-8">
      <div className="container">
        <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <p className="text-sm text-muted-foreground">
            RegulationCoder &mdash; AI-powered compliance analysis for the EU AI Act
          </p>
          <p className="text-xs text-muted-foreground/50">
            Powered by Anthropic Claude
          </p>
        </div>
      </div>
    </footer>
  );
}
