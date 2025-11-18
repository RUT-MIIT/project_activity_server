import type { FC } from 'react';
import type { IFormTextareaProps } from '../../types/types';

import styles from './form-textarea.module.scss';

export const FormTextarea: FC<IFormTextareaProps> = ({
	name,
	placeholder = 'Введите значение..',
	value,
	onChange,
}) => {
	return (
		<textarea
			className={styles.textarea}
			name={name}
			id={`id-${name}`}
			value={value}
			onChange={onChange}
			placeholder={placeholder}
			autoComplete='off'
		/>
	);
};
