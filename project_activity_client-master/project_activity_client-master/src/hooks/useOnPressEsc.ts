import { useEffect } from 'react';

type TKeyEventHandler = (event: KeyboardEvent) => void;

export const useOnPressEsc = (handler?: TKeyEventHandler) => {
	useEffect(() => {
		if (!handler) {
			return;
		}

		const listener = (event: KeyboardEvent) => {
			if (event.key === 'Escape') {
				handler(event);
			}
		};

		document.addEventListener('keydown', listener);

		return () => {
			document.removeEventListener('keydown', listener);
		};
	}, [handler]);
};
