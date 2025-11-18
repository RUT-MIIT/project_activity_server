import type { FC, FormEvent } from 'react';
import type { IRegistrationForm } from '../types/types';

import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from '../../../store/store';
import { useForm } from '../../../hooks/useForm';

import { PublicLayout } from '../../../shared/components/Layout/PublicLayout/ui/public-layout';
import { Form } from '../../../shared/components/Form/ui/form';
import {
	FormField,
	FormInput,
	FormTextarea,
	FormButtons,
	FormLinks,
} from '../../../shared/components/Form/components';
import { Button } from '../../../shared/components/Button/ui/button';

import {
	links,
	initialRegistrationValues,
	validationSchema,
	shouldBlockSubmit,
} from '../lib/helpers';

import { registerUser } from '../../../store/user/actions';

import styles from '../styles/registration.module.scss';

export const Registration: FC = () => {
	const dispatch = useDispatch();
	const { isLoading } = useSelector((state) => state.user);
	const [isBlockSubmit, setIsBlockSubmit] = useState<boolean>(true);
	const { values, handleChange, errors } = useForm<IRegistrationForm>(
		initialRegistrationValues,
		validationSchema
	);

	const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		if (!isBlockSubmit) {
			dispatch(
				registerUser({
					email: values.email,
					first_name: values.firstName,
					last_name: values.lastName,
					middle_name: values.middleName,
					phone: values.phone,
					comment: values.comment,
				})
			);
		}
	};

	useEffect(() => {
		setIsBlockSubmit(shouldBlockSubmit(values, errors));
	}, [values, errors]);

	return (
		<PublicLayout>
			<main className={styles.container}>
				<Form
					name='form-registration'
					onSubmit={handleSubmit}
					title='Присоединяйтесь к проектам!'
					subtitle='Зарегистрируйтесь, чтобы начать участие в проектной деятельности'
					titleAlign='left'>
					<FormField
						title='Фамилия'
						fieldError={{
							text: errors.lastName || '',
							isShow: !!errors.lastName,
						}}>
						<FormInput
							name='lastName'
							placeholder='Ваша фамилия'
							value={values.lastName}
							onChange={handleChange}
						/>
					</FormField>
					<FormField
						title='Имя'
						fieldError={{
							text: errors.firstName || '',
							isShow: !!errors.firstName,
						}}>
						<FormInput
							name='firstName'
							placeholder='Ваше имя'
							value={values.firstName}
							onChange={handleChange}
						/>
					</FormField>
					<FormField
						title='Отчество'
						fieldError={{
							text: errors.middleName || '',
							isShow: !!errors.middleName,
						}}>
						<FormInput
							name='middleName'
							placeholder='Ваше отчество'
							value={values.middleName}
							onChange={handleChange}
						/>
					</FormField>

					<FormField
						title='Электронная почта'
						fieldError={{ text: errors.email || '', isShow: !!errors.email }}>
						<FormInput
							name='email'
							placeholder='Ваша электронная почта'
							value={values.email}
							onChange={handleChange}
						/>
					</FormField>
					<FormField
						title='Телефон'
						fieldError={{
							text: errors.phone || '',
							isShow: !!errors.phone,
						}}>
						<FormInput
							name='phone'
							placeholder='+ 7'
							value={values.phone}
							onChange={handleChange}
						/>
					</FormField>
					<FormField title='Комментарий'>
						<FormTextarea
							name='comment'
							placeholder='Опишите цель регистрации'
							value={values.comment}
							onChange={handleChange}
						/>
					</FormField>
					<FormButtons>
						<Button
							type='submit'
							text='Зарегистрироваться'
							width='full'
							isBlock={isBlockSubmit || isLoading}></Button>
					</FormButtons>
				</Form>
				<FormLinks links={links} />
			</main>
		</PublicLayout>
	);
};
