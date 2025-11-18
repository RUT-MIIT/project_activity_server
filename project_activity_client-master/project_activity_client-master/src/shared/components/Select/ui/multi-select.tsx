import type { IMultiSelectProps } from '../types/types';

import { useState, useEffect, useRef } from 'react';

import { Checkbox } from '../../Checkbox/ui/checkbox';

import { useOnClickOutside } from '../../../../hooks/useOnClickOutside';

import styles from '../styles/select.module.scss';

export const MultiSelect = <T,>({
	options,
	selectedOptions,
	onChange,
	valueKey = 'id' as keyof T,
	labelKey = 'name' as keyof T,
	placeholder = 'Выберите из списка...',
}: IMultiSelectProps<T>) => {
	const [isOpen, setIsOpen] = useState(false);
	const selectRef = useRef<HTMLDivElement>(null);

	const toggleSelect = () => setIsOpen((prev) => !prev);
	const closeSelect = () => setIsOpen(false);

	useOnClickOutside(selectRef, closeSelect);

	useEffect(() => {
		closeSelect();
	}, []);

	const getValue = (item: T) => String(item[valueKey]);
	const getLabel = (item: T) => String(item[labelKey]);

	const handleToggleOption = (option: T) => {
		const keyValue = getValue(option);
		const alreadySelected = selectedOptions.some(
			(o) => getValue(o) === keyValue
		);

		if (alreadySelected) {
			onChange(selectedOptions.filter((o) => getValue(o) !== keyValue));
		} else {
			onChange([...selectedOptions, option]);
		}
	};

	const getSelectedText = () => {
		if (selectedOptions.length === 0) return placeholder;
		if (selectedOptions.length === 1) return getLabel(selectedOptions[0]);
		return `Выбрано: ${selectedOptions.length}`;
	};

	return (
		<div
			ref={selectRef}
			className={`${styles.select} ${isOpen ? styles.select_status_open : ''}`}
			onClick={toggleSelect}>
			<div className={styles.main}>
				<p
					className={`${styles.title} ${
						selectedOptions.length === 0 ? styles.text_empty : ''
					}`}>
					{getSelectedText()}
				</p>
				<div
					className={`${styles.arrow} ${
						isOpen ? styles.arrow_status_open : ''
					}`}
				/>
			</div>

			<div
				className={`${styles.options} ${
					isOpen ? styles.options_status_open : ''
				}`}>
				<ul className={styles.list}>
					{options.length > 0 ? (
						options.map((item) => {
							const checked = selectedOptions.some(
								(o) => getValue(o) === getValue(item)
							);

							return (
								<li
									key={getValue(item)}
									className={`${styles.item} ${styles.item_type_select} ${
										checked ? styles.item_selected : ''
									}`}
									onClick={(e) => e.stopPropagation()}>
									<Checkbox
										checked={checked}
										label={getLabel(item)}
										onChange={() => handleToggleOption(item)}
									/>
								</li>
							);
						})
					) : (
						<li className={styles.item}>
							<p className={`${styles.text} ${styles.text_empty}`}>
								Результаты не найдены.
							</p>
						</li>
					)}
				</ul>
			</div>
		</div>
	);
};
