import type { FC } from 'react';
import type { ICardProps } from '../types/types';

import styles from '../styles/card.module.scss';

export const Card: FC<ICardProps> = ({
	title,
	subtitle,
	withHeightStretch,
	children,
}) => {
	return (
		<div
			className={`${styles.card} ${
				withHeightStretch ? styles.card_height_stretch : ''
			}`}>
			{title && <h2 className={styles.title}>{title}</h2>}
			{subtitle && <p className={styles.subtitle}>{subtitle}</p>}
			{children}
		</div>
	);
};
