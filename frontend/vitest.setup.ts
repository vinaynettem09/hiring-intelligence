import "@testing-library/jest-dom/vitest";

// jsdom lacks a few browser APIs that our components + Radix primitives touch. Polyfill the
// minimum so component tests run realistically (theme matchMedia, Radix pointer/resize, and
// the Blob URL used by the timeline CSV export).
type Writable = Record<string, unknown>;

if (!window.matchMedia) {
  window.matchMedia = ((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => false,
  })) as typeof window.matchMedia;
}

if (!("ResizeObserver" in window)) {
  (window as Writable).ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
}

const proto = Element.prototype as unknown as Writable;
proto.hasPointerCapture ??= () => false;
proto.setPointerCapture ??= () => {};
proto.releasePointerCapture ??= () => {};
proto.scrollIntoView ??= () => {};

if (!URL.createObjectURL) URL.createObjectURL = () => "blob:mock";
if (!URL.revokeObjectURL) URL.revokeObjectURL = () => {};
