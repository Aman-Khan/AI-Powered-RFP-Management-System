import { useEffect } from "react";

export function useTypewriter({
  text,
  speed = 15,
  onUpdate,
  onDone
}: {
  text: string;
  speed?: number;
  onUpdate: (v: string) => void;
  onDone?: () => void;
}) {
  useEffect(() => {
    if (!text) return;

    let index = 0;
    let cancelled = false;

    function typeNext() {
      if (cancelled) return;

      onUpdate(text.slice(0, index + 1));

      index++;

      if (index < text.length) {
        setTimeout(typeNext, speed);
      } else {
        onDone && onDone();
      }
    }

    typeNext();

    return () => {
      cancelled = true;
    };
  }, [text]);
}
