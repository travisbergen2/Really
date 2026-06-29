export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <title>RPCS-1 Hub</title>
      </head>
      <body>
        <main className="max-w-4xl mx-auto p-4">
          <h1 className="text-2xl font-bold mb-4">RPCS‑1 Hub</h1>
          {children}
        </main>
      </body>
    </html>
  );
}
