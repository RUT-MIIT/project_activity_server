import type { FC } from 'react';
import type { IModalProps } from '../types/types';

import ReactDOM from 'react-dom';

import { useOnPressEsc } from '../../../../hooks/useOnPressEsc';

import { ModalOverlay } from './modal-overlay';

import styles from '../styles/modal.module.scss';

export const Modal: FC<IModalProps> = ({
	isOpen,
	onClose,
	title,
	description,
	modalWidth = 'default',
	closeByClickOutside = true,
	closeByPressEsc = true,
	children,
}) => {
	const modalRoot = document.getElementById('modal-root');

	useOnPressEsc(closeByPressEsc ? onClose : undefined);

	const handleOverlayClick = () => {
		if (closeByClickOutside) {
			onClose();
		}
	};

	const modalContent = (
		<div className={`${styles.modal} ${isOpen ? styles.modal_opened : ''}`}>
			{isOpen && <ModalOverlay onClick={handleOverlayClick} />}
			<div
				className={`${styles.container} ${
					styles[`container_width_${modalWidth}`]
				}`}>
				<button
					className={styles.close}
					type='button'
					onClick={onClose}></button>
				{title && <h2 className={styles.title}>{title || ''}</h2>}
				{description && (
					<p className={styles.description}>{description || ''}</p>
				)}
				{children}
			</div>
		</div>
	);

	return ReactDOM.createPortal(modalContent, modalRoot || document.body);
};
