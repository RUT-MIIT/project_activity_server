import type { FC } from 'react';
import type { ITextTemplateProps } from '../types/types';

import styles from '../styles/text-template.module.scss';

export const TextTemplate: FC<ITextTemplateProps> = ({ text }) => {
	const paragraphs = text.split(/\r?\n/);

	return (
		<div className={styles.container}>
			{paragraphs.map((paragraph, index) => (
				<p key={index} className={styles.text}>
					{paragraph}
				</p>
			))}
		</div>
	);
};
