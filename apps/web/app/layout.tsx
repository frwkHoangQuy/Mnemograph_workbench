import type { ReactNode } from "react";

export const metadata = {
  title: "Mnemograph Workbench",
  description: "Phase 0 placeholder for the Mnemograph Workbench web app",
};

type RootLayoutProps = Readonly<{
  children: ReactNode;
}>;

export default function RootLayout({ children }: RootLayoutProps): ReactNode {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
