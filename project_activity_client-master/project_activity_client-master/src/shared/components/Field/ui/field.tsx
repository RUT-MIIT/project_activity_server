import type { FC } from 'react';
import type { IFieldProps } from '../types/types';

import styles from '../styles/field.module.scss';

export const Field: FC<IFieldProps> = ({ title, text }) => {
	return (
		<div className={styles.container}>
			{title && <h4 className={styles.title}>{title}</h4>}
			<div className={styles.field}>
				<p className={styles.text}>{text}</p>
			</div>
		</div>
	);
};
