import type { FC } from 'react';
import type { IFormInputProps } from '../../types/types';

import styles from './form-input.module.scss';

export const FormInput: FC<IFormInputProps> = ({
	type = 'text',
	name,
	placeholder = 'Введите значение..',
	value,
	onChange,
}) => {
	return (
		<input
			className={styles.input}
			type={type}
			name={name}
			id={`id-${name}`}
			value={value}
			onChange={onChange}
			placeholder={placeholder}
			autoComplete='off'
		/>
	);
};
