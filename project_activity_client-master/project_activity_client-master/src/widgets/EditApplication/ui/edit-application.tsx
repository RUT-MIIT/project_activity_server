import type { FC, FormEvent } from 'react';
import type { IEditAppForm } from '../types/types';
import type { IInstitute } from '../../../store/catalog/types';
import type { IProjectLevel } from '../../../shared/lib/lib';
import type {
	IApplicationComment,
	IField,
} from '../../../store/application/types';

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from '../../../store/store';
import { useForm } from '../../../hooks/useForm';

import { Button } from '../../../shared/components/Button/ui/button';
import { Tabs } from '../../../shared/components/Tabs/ui/tabs';
import { Card } from '../../../shared/components/Card/ui/card';
import { Form } from '../../../shared/components/Form/ui/form';
import {
	FormInput,
	FormTextarea,
} from '../../../shared/components/Form/components';
import { Preloader } from '../../../shared/components/Preloader/ui/preloader';
import { Select } from '../../../shared/components/Select/ui/select';
import { ApplicationField } from './application-field';
import { ApplicationComments } from './application-comments';
import { MultiSelect } from '../../../shared/components/Select/ui/multi-select';

import {
	validationSchema,
	initialAppValues,
	shouldBlockSubmit,
} from '../lib/helpers';
import {
	editAppAction,
	approveAppAction,
	reworkAppAction,
	rejectAppAction,
} from '../../../store/coordination/actions';
import { getInstitutesAction } from '../../../store/catalog/actions';
import { setCurrentField } from '../../../store/coordination/reducer';
import { projectLevels } from '../../../shared/lib/lib';
import { EPAGESROUTES, EMAINROUTES } from '../../../shared/utils/routes';

import styles from '../styles/edit-application.module.scss';

export const EditApplication: FC = () => {
	const navigate = useNavigate();
	const dispatch = useDispatch();

	const { user } = useSelector((state) => state.user);
	const { applicationDetail, currentField } = useSelector(
		(state) => state.coordination
	);
	const { institutes, isLoadingCatalog } = useSelector(
		(state) => state.catalog
	);

	const [activeTab, setActiveTab] = useState('/description');
	const [isBlockSubmit, setIsBlockSubmit] = useState<boolean>(true);
	const { values, handleChange, handleSelectChange, errors, setValues } =
		useForm<IEditAppForm>(initialAppValues, validationSchema);

	const getCommentCount = (fieldName: string) => {
		return (
			applicationDetail?.comments?.filter(
				(comment: IApplicationComment) => comment.field === fieldName
			).length || 0
		);
	};

	const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		if (!isBlockSubmit && user && applicationDetail) {
			const appData = {
				...values,
				project_level:
					typeof values.project_level === 'object'
						? values.project_level.name
						: values.project_level,
				target_institutes: values.target_institutes.map((elem) => elem.code),
			};

			try {
				await dispatch(
					editAppAction({ id: applicationDetail.id, data: appData })
				).unwrap();
				console.log('Успешно');
			} catch (err) {
				console.error('Ошибка при создании заявки:', err);
			}
		}
	};

	const handleApproveApp = async () => {
		if (user && applicationDetail) {
			try {
				await dispatch(
					approveAppAction({ applicationId: applicationDetail.id })
				).unwrap();
				navigate(`${EPAGESROUTES.MAIN}/${EMAINROUTES.COORDINATION}`, {
					replace: true,
				});
			} catch (err) {
				console.error('Ошибка при согласовании заявки:', err);
			}
		}
	};

	const handleReworkApp = async () => {
		if (user && applicationDetail) {
			try {
				await dispatch(
					reworkAppAction({ applicationId: applicationDetail.id })
				).unwrap();
				navigate(`${EPAGESROUTES.MAIN}/${EMAINROUTES.COORDINATION}`, {
					replace: true,
				});
			} catch (err) {
				console.error('Ошибка при доработке заявки:', err);
			}
		}
	};

	const handleRejectApp = async (reason: string) => {
		if (user && applicationDetail) {
			try {
				await dispatch(
					rejectAppAction({
						applicationId: applicationDetail.id,
						reason: reason,
					})
				).unwrap();
				navigate(`${EPAGESROUTES.MAIN}/${EMAINROUTES.COORDINATION}`, {
					replace: true,
				});
			} catch (err) {
				console.error('Ошибка при отклонении заявки:', err);
			}
		}
	};

	const handleChangeInstitute = (selected: IInstitute[]) => {
		handleSelectChange('target_institutes', selected);
	};

	const handleChangeLevel = (selected: IProjectLevel) => {
		handleSelectChange('project_level', selected);
	};

	const handleSelectField = (selected: IField) => {
		dispatch(setCurrentField(selected));
	};

	const hasAction = (actionName: string) =>
		applicationDetail?.available_actions.some((a) => a.action === actionName);

	useEffect(() => {
		setIsBlockSubmit(shouldBlockSubmit(values, errors));
	}, [values, errors]);

	useEffect(() => {
		dispatch(setCurrentField(null));
		dispatch(getInstitutesAction());
	}, [dispatch]);

	useEffect(() => {
		if (applicationDetail) {
			const levelOption =
				projectLevels.find(
					(level) => level.name === applicationDetail.project_level
				) || projectLevels[0];

			setValues({
				title: applicationDetail.title || '',
				company: applicationDetail.company || '',
				company_contacts: applicationDetail.company_contacts || '',
				project_level: levelOption,
				target_institutes: applicationDetail.target_institutes || [],
				problem_holder: applicationDetail.problem_holder || '',
				goal: applicationDetail.goal || '',
				barrier: applicationDetail.barrier || '',
				existing_solutions: applicationDetail.existing_solutions || '',
				context: applicationDetail.context || '',
				recommended_tools: applicationDetail.recommended_tools || '',
				stakeholders: applicationDetail.stakeholders || '',
				experts: applicationDetail.experts || '',
				additional_materials: applicationDetail.additional_materials || '',
			});
		}
	}, [applicationDetail, setValues]);

	if (isLoadingCatalog) {
		return <Preloader />;
	}

	return (
		<div className={styles.container}>
			<div className={styles.header}>
				<Tabs
					tabs={[
						{ path: '/description', label: 'О проекте' },
						{ path: '/problem', label: 'Проблема' },
						{ path: '/context', label: 'Контекст' },
						{ path: '/additional', label: 'Дополнительно' },
					]}
					activeTab={activeTab}
					onTabChange={(path) => setActiveTab(path)}
				/>
				<Button
					text='Вернуться'
					withIcon={{ type: 'back', color: 'black' }}
					onClick={() => navigate(-1)}
				/>
			</div>

			<div className={styles.main}>
				<div className={styles.form}>
					<Card withHeightStretch>
						<Form
							name='form-edit-app'
							onSubmit={handleSubmit}
							formWidth='full'
							withHeightStretch>
							<div className={styles.form__content}>
								{activeTab === '/description' && (
									<>
										<ApplicationField
											title='Наименование проекта'
											fieldCode='title'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<FormInput
												name='title'
												value={values.title}
												onChange={handleChange}
												placeholder='Введите наименование проекта'
											/>
										</ApplicationField>
										<ApplicationField
											title='Наименование организации-заказчика'
											fieldCode='company'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<FormInput
												name='company'
												value={values.company}
												onChange={handleChange}
												placeholder='Введите наименование организации-заказчика'
											/>
										</ApplicationField>
										<ApplicationField
											title='Контактные данные представителя заказчика'
											fieldCode='company_contacts'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<FormTextarea
												name='company_contacts'
												value={values.company_contacts}
												onChange={handleChange}
												placeholder='Введите контактные данные'
											/>
										</ApplicationField>
										<ApplicationField
											title='Уровень проекта'
											fieldCode='project_level'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<Select
												options={projectLevels}
												currentOption={values.project_level}
												onChooseOption={handleChangeLevel}
											/>
										</ApplicationField>
										<ApplicationField
											title='Экспертам из какого института / академии обратить внимание'
											fieldCode='target_institutes'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<MultiSelect
												options={institutes}
												selectedOptions={values.target_institutes}
												valueKey='code'
												labelKey='name'
												onChange={handleChangeInstitute}
											/>
										</ApplicationField>
									</>
								)}
								{activeTab === '/problem' && (
									<>
										<ApplicationField
											title='Носитель проблемы'
											fieldCode='problem_holder'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<FormInput
												name='problem_holder'
												value={values.problem_holder}
												onChange={handleChange}
												placeholder='Введите носителя проблемы'
											/>
										</ApplicationField>
										<ApplicationField
											title='Цель'
											fieldCode='goal'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<FormTextarea
												name='goal'
												value={values.goal}
												onChange={handleChange}
												placeholder='Введите цель проекта'
											/>
										</ApplicationField>
										<ApplicationField
											title='Барьер'
											fieldCode='barrier'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<FormTextarea
												name='barrier'
												value={values.barrier}
												onChange={handleChange}
												placeholder='Что мешает решить проблему сейчас?'
											/>
										</ApplicationField>
										<ApplicationField
											title='Существующие решения'
											fieldCode='existing_solutions'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<FormTextarea
												name='existing_solutions'
												value={values.existing_solutions}
												onChange={handleChange}
												placeholder='Введите существующие решения'
											/>
										</ApplicationField>
									</>
								)}
								{activeTab === '/context' && (
									<>
										<ApplicationField
											title='Контекст проекта'
											fieldCode='context'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<FormTextarea
												name='context'
												value={values.context}
												onChange={handleChange}
												placeholder='Введите контекст проекта'
											/>
										</ApplicationField>
										<ApplicationField
											title='Другие заинтересованные стороны'
											fieldCode='stakeholders'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<FormTextarea
												name='stakeholders'
												value={values.stakeholders}
												onChange={handleChange}
												placeholder='Введите другие заинтересованные стороны'
											/>
										</ApplicationField>
										<ApplicationField
											title='Рекомендуемые инструменты / методы'
											fieldCode='recommended_tools'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<FormTextarea
												name='recommended_tools'
												value={values.recommended_tools}
												onChange={handleChange}
												placeholder='Введите рекомендуемые инструменты / методы'
											/>
										</ApplicationField>
										<ApplicationField
											title='Эксперты'
											fieldCode='experts'
											currentField={currentField}
											getCommentCount={getCommentCount}
											onSelectField={handleSelectField}>
											<FormTextarea
												name='experts'
												value={values.experts}
												onChange={handleChange}
												placeholder='Введите экспертов'
											/>
										</ApplicationField>
									</>
								)}
								{activeTab === '/additional' && (
									<ApplicationField
										title='Дополнительные материалы'
										fieldCode='additional_materials'
										currentField={currentField}
										getCommentCount={getCommentCount}
										onSelectField={handleSelectField}>
										<FormTextarea
											name='additional_materials'
											value={values.additional_materials}
											onChange={handleChange}
											placeholder='Введите дополнительные материалы'
										/>
									</ApplicationField>
								)}
							</div>
							<div className={styles.form__control}>
								{hasAction('save_changes') && (
									<Button
										text='Сохранить'
										type='submit'
										color='green'
										withIcon={{ type: 'check', color: 'white' }}
									/>
								)}
								{hasAction('approve') && (
									<Button
										text='Согласовать'
										color='blue'
										withIcon={{ type: 'send', color: 'white' }}
										onClick={handleApproveApp}
									/>
								)}
								{hasAction('request_changes') && (
									<Button
										text='Вернуть'
										withIcon={{ type: 'return', color: 'black' }}
										onClick={handleReworkApp}
									/>
								)}
								{hasAction('reject') && (
									<Button
										text='Отклонить'
										color='red'
										withIcon={{ type: 'cancel', color: 'white' }}
										onClick={() => handleRejectApp('Test')}
									/>
								)}
							</div>
						</Form>
					</Card>
				</div>
				<div className={styles.comments}>
					<Card withHeightStretch>
						<ApplicationComments />
					</Card>
				</div>
			</div>
		</div>
	);
};
