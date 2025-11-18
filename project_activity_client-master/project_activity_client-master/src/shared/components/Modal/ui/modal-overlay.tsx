import type { FC } from 'react';
import type { IModalOverlayProps } from '../types/types';

import styles from '../styles/modal.module.scss';

export const ModalOverlay: FC<IModalOverlayProps> = ({ onClick }) => {
	return <div className={styles.overlay} onClick={onClick} />;
};
