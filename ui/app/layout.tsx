import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "MTG Strategist - Magic: The Gathering Deck Building Assistant",
  description: "Get expert advice on Magic: The Gathering deck building strategies, card synergies, and gameplay tips.",
  keywords: ["Magic: The Gathering", "MTG", "deck building", "card game", "strategy", "card synergies"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.variable} font-sans h-full`}>
        {children}
      </body>
    </html>
  );
}