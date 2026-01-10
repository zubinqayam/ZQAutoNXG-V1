import "./globals.css";
import { Inter } from "next/font/google";
import type { Metadata } from "next";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "ZQAutoNXG - Next-Generation Automation Platform",
  description: "Next-Generation eXtended Automation Platform powered by ZQ AI LOGIC™",
  metadataBase: new URL("http://localhost:3000"),
  openGraph: {
    title: "ZQAutoNXG - Next-Generation Automation Platform",
    description: "Next-Generation eXtended Automation Platform powered by ZQ AI LOGIC™",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "ZQAutoNXG - Next-Generation Automation Platform",
    description: "Next-Generation eXtended Automation Platform powered by ZQ AI LOGIC™",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="min-h-screen bg-gradient-to-br from-primary-400 via-purple-500 to-primary-600">
        {children}
      </body>
    </html>
  );
}
