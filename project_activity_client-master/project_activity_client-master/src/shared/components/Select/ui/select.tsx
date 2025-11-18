import type { ISelectProps } from '../types/types';

import { useState, useEffect, useRef } from 'react';
import { useOnClickOutside } from '../../../../hooks/useOnClickOutside';

import styles from '../styles/select.module.scss';

export const Select = <T,>({
	options,
	currentOption,
	onChooseOption,
	valueKey = 'id' as keyof T,
	labelKey = 'name' as keyof T,
	placeholder = 'Выберите значение...',
}: ISelectProps<T>) => {
	const [isOpenSelectOptions, setIsOpenSelectOptions] = useState(false);
	const selectRef = useRef<HTMLDivElement>(null);

	const openSelectOptions = () => {
		setIsOpenSelectOptions(!isOpenSelectOptions);
	};

	const chooseOption = (option: T) => {
		onChooseOption(option);
		setIsOpenSelectOptions(false);
	};

	const handleClickOutside = () => {
		setIsOpenSelectOptions(false);
	};

	useOnClickOutside(selectRef, handleClickOutside);

	useEffect(() => {
		setIsOpenSelectOptions(false);
	}, []);

	const getValue = (item: T) => String(item[valueKey]);
	const getLabel = (item: T) => String(item[labelKey]);

	return (
		<div
			ref={selectRef}
			className={`${styles.select} ${
				isOpenSelectOptions ? styles.select_open : ''
			}`}
			onClick={openSelectOptions}>
			<div className={styles.main}>
				<p
					className={`${styles.title} ${
						!currentOption || getValue(currentOption) === '0'
							? styles.text_empty
							: ''
					}`}>
					{currentOption ? getLabel(currentOption) : placeholder}
				</p>
				<div
					className={`${styles.arrow} ${
						isOpenSelectOptions ? styles.arrow_status_open : ''
					}`}
				/>
			</div>
			<div
				className={`${styles.options} ${
					isOpenSelectOptions ? styles.options_status_open : ''
				}`}>
				<ul className={styles.list}>
					{options.length > 0 ? (
						options
							.filter(
								(item) =>
									getValue(item) !== getValue(currentOption ?? ({} as T))
							)
							.map((item) => (
								<li
									className={styles.item}
									key={getValue(item)}
									onClick={() => chooseOption(item)}>
									<p className={styles.text}>{getLabel(item)}</p>
								</li>
							))
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
