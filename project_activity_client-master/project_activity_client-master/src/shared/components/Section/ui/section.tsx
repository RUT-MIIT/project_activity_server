import type { FC } from 'react';
import type { ISectionProps } from '../types/types';

import styles from '../styles/section.module.scss';

export const Section: FC<ISectionProps> = ({
	sectionTitle,
	sectionDescription,
	withHeaderMargin,
	children,
}) => {
	return (
		<section className={styles.section}>
			{sectionTitle && (
				<div
					className={`${styles.header} ${
						withHeaderMargin ? styles.header_mb_20 : ''
					}`}>
					<h2 className={styles.title}>{sectionTitle.text}</h2>
					{sectionDescription && (
						<p className={styles.subtitle}>{sectionDescription}</p>
					)}
				</div>
			)}
			{children}
		</section>
	);
};
