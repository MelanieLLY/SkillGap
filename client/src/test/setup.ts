/* eslint-disable no-undef */
/* eslint-disable @typescript-eslint/no-var-requires */
/// <reference types="vitest/globals" />
import React from "react";
import "@testing-library/jest-dom";
import { vi } from "vitest";

// ── Mock framer-motion globally ───────────────────────────────────────────────
// framer-motion uses browser APIs (RAF, CSS, SVG) that jsdom doesn't support.
// We replace all animated components with plain HTML equivalents so tests
// exercise rendering logic and props, not the animation engine itself.
vi.mock("framer-motion", () => {
  // Use React from the local scope if available or re-import it safely.
  // In Vitest factories, you can use imports if they are mocked or hoisted.
  const React = require("react");

  type MotionProps = {
    children?: React.ReactNode;
    [key: string]: unknown;
  };

  // Generic passthrough that strips framer-motion-specific props
  const MotionComponent = (tag: string) =>
    React.forwardRef(
      (
        {
          children,
          animate: _animate,
          initial: _initial,
          exit: _exit,
          transition: _transition,
          variants: _variants,
          whileHover: _whileHover,
          whileTap: _whileTap,
          style,
          ...rest
        }: MotionProps & { style?: React.CSSProperties },
        ref: React.Ref<unknown>
      ) =>
        React.createElement(tag, { ...rest, style, ref }, children)
    );

  // useSpring: return a plain object with set / on methods
  const useSpring = (initial: number) => {
    let value = initial;
    const subscribers: Array<(v: number) => void> = [];
    return {
      get: () => value,
      set: (v: number) => {
        value = v;
        subscribers.forEach((cb) => cb(v));
      },
      on: (_event: string, cb: (v: number) => void) => {
        subscribers.push(cb);
        return () => {
          const idx = subscribers.indexOf(cb);
          if (idx > -1) subscribers.splice(idx, 1);
        };
      },
    };
  };

  // useTransform: return a MotionValue-like object whose value is derived
  const useTransform = (
    _source: unknown,
    _input: number[],
    output: number[]
  ) => ({
    get: () => output[0],
  });

  return {
    motion: {
      div: MotionComponent("div"),
      span: MotionComponent("span"),
      circle: MotionComponent("circle"),
      ul: MotionComponent("ul"),
      li: MotionComponent("li"),
    },
    AnimatePresence: ({ children }: { children: React.ReactNode }) =>
      React.createElement(React.Fragment, null, children),
    useSpring,
    useTransform,
  };
});

// ── Silence console.error noise from expected error tests ────────────────────
const originalConsoleError = console.error;
beforeAll(() => {
  console.error = (...args: unknown[]) => {
    // Suppress React prop-type / framer-motion errors in tests
    if (
      typeof args[0] === "string" &&
      (args[0].includes("Warning:") || args[0].includes("framer-motion"))
    ) {
      return;
    }
    originalConsoleError(...args);
  };
});

afterAll(() => {
  console.error = originalConsoleError;
});
