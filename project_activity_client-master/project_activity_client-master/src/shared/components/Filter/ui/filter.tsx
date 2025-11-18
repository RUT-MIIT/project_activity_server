import type { ChangeEvent } from 'react';
import type { IFilterProps } from '../types/types';
import { useState } from 'react';

import styles from '../styles/filter.module.scss';

export const Filter = <T,>({
	data,
	searchKey,
	placeholder = 'Поиск...',
	onFilter,
}: IFilterProps<T>) => {
	const [query, setQuery] = useState('');

	const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
		const value = e.target.value;
		setQuery(value);

		const filtered = data.filter((item) => {
			const fieldValue = item[searchKey];
			return (
				typeof fieldValue === 'string' &&
				fieldValue.toLowerCase().includes(value.toLowerCase())
			);
		});

		onFilter(filtered);
	};

	return (
		<input
			className={styles.filter}
			type='text'
			placeholder={placeholder}
			value={query}
			onChange={handleChange}
		/>
	);
};
