import { useEffect } from 'react';

type TEventHandler = (event: MouseEvent | TouchEvent) => void;

export const useOnClickOutside = (
	ref: React.RefObject<HTMLElement>,
	handler?: TEventHandler
) => {
	useEffect(() => {
		if (!handler) {
			return;
		}
		const listener = (event: MouseEvent | TouchEvent) => {
			if (!ref.current || ref.current.contains(event.target as Node)) {
				return;
			}
			handler(event);
		};
		document.addEventListener('mousedown', listener);
		return () => {
			document.removeEventListener('mousedown', listener);
		};
	}, [ref, handler]);
};
