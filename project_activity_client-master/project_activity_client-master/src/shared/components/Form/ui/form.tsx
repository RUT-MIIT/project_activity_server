import type { FC } from 'react';
import type { IFormProps } from '../types/types';

import styles from '../styles/form.module.scss';

export const Form: FC<IFormProps> = ({
	title,
	subtitle,
	titleAlign = 'left',
	formWidth = 'full',
	withHeightStretch = false,
	name,
	onSubmit,
	children,
}) => {
	return (
		<form
			className={`${styles.container} ${
				styles[`container_width_${formWidth}`]
			} ${withHeightStretch ? styles.container_height_stretch : ''}`}
			name={name}
			id={name}
			onSubmit={onSubmit}
			noValidate>
			{title && (
				<h2
					className={`${styles.title} ${styles[`title_align_${titleAlign}`]}`}>
					{title}
				</h2>
			)}
			{subtitle && (
				<p
					className={`${styles.subtitle} ${
						styles[`subtitle_align_${titleAlign}`]
					}`}>
					{subtitle}
				</p>
			)}
			{children}
		</form>
	);
};
