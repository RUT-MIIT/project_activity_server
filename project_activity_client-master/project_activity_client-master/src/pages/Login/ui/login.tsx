import type { FC, FormEvent } from 'react';
import type { ILoginForm } from '../types/types';

import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from '../../../store/store';
import { useForm } from '../../../hooks/useForm';

import { PublicLayout } from '../../../shared/components/Layout/PublicLayout/ui/public-layout';
import { Form } from '../../../shared/components/Form/ui/form';
import {
	FormField,
	FormInput,
	FormButtons,
	FormLinks,
} from '../../../shared/components/Form/components';
import { Button } from '../../../shared/components/Button/ui/button';

import { links, validationSchema, shouldBlockSubmit } from '../lib/helpers';

import { loginUser } from '../../../store/user/actions';

import styles from '../styles/login.module.scss';

export const Login: FC = () => {
	const dispatch = useDispatch();
	const { isLoading } = useSelector((state) => state.user);
	const [isBlockSubmit, setIsBlockSubmit] = useState<boolean>(true);
	const { values, handleChange, errors } = useForm<ILoginForm>(
		{ email: '', password: '' },
		validationSchema
	);

	const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		if (!isBlockSubmit) {
			dispatch(loginUser(values));
		}
	};

	useEffect(() => {
		setIsBlockSubmit(shouldBlockSubmit(values, errors));
	}, [values, errors]);

	return (
		<PublicLayout>
			<main className={styles.container}>
				<Form
					name='form-login'
					onSubmit={handleSubmit}
					title='С возвращением!'
					subtitle='Войдите в свой аккаунт, чтобы продолжить работу над проектами'
					titleAlign='left'>
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
						title='Пароль'
						fieldError={{
							text: errors.password || '',
							isShow: !!errors.password,
						}}>
						<FormInput
							name='password'
							placeholder='Ваш пароль'
							value={values.password}
							onChange={handleChange}
						/>
					</FormField>
					<FormButtons>
						<Button
							type='submit'
							text='Войти'
							width='full'
							color='blue'
							isBlock={isBlockSubmit || isLoading}
						/>
					</FormButtons>
				</Form>
				<FormLinks links={links} />
			</main>
		</PublicLayout>
	);
};
