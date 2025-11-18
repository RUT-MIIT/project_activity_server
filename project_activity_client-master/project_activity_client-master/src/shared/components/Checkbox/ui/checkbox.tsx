import type { FC } from 'react';
import type { ICheckboxProps } from '../types/types';

import styles from '../styles/checkbox.module.scss';

export const Checkbox: FC<ICheckboxProps> = ({
	checked,
	label,
	onChange,
	disabled = false,
}) => {
	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		onChange(e.target.checked);
	};

	return (
		<label
			className={styles.checkbox_label}
			onClick={(e) => e.stopPropagation()}>
			<input
				type='checkbox'
				checked={checked}
				disabled={disabled}
				onChange={handleChange}
				className={styles.checkbox}
			/>
			{label && <span className={styles.text}>{label}</span>}
		</label>
	);
};
