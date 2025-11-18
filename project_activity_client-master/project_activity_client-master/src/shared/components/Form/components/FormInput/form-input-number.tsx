import type { FC } from 'react';
import type { IFormInputNumberProps } from '../../types/types';

import styles from './form-input.module.scss';

export const FormInputNumber: FC<IFormInputNumberProps> = ({
	type = 'number',
	name,
	placeholder = 'Введите число..',
	value,
	onChange,
}) => {
	return (
		<input
			className={styles.input}
			type={type}
			name={name}
			id={`id-${name}`}
			value={value || ''}
			onChange={onChange}
			placeholder={placeholder}
			autoComplete='off'
		/>
	);
};
