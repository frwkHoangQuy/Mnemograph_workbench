import { afterEach, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";

afterEach(() => {
  cleanup();
});

it("renders the workbench heading", async () => {
  const { default: Page } = await import("./page");
  render(<Page />);

  expect(
    screen.getByRole("heading", { name: "Mnemograph Workbench" }),
  ).toBeTruthy();
});
