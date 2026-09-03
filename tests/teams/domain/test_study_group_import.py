"""Тесты доменной логики импорта учебных групп из контингента."""

from __future__ import annotations

import pytest

from teams.domain.study_group_import import (
    ExistingGroupCandidate,
    build_group_import_row,
    collect_teaching_group_names_in_file,
    get_study_group_override_by_external_id,
    is_skipped_permanent_group,
    is_skipped_study_group_name,
    map_teaching_group_name_for_lookup,
    normalize_external_group_id,
    parse_course_from_teaching_group_name,
    remap_external_group_id,
    resolve_existing_group_for_id,
    resolve_study_group_display_name,
)


class TestStudyGroupIdImportDomain:
    def test_parse_course_from_teaching_group_name(self) -> None:
        assert parse_course_from_teaching_group_name("ТПВг-341") == 3
        assert parse_course_from_teaching_group_name("АМБ-211") == 2

    def test_build_group_import_row_by_external_id(self) -> None:
        row = build_group_import_row(
            permanent_group_code="АМБ-2025-11",
            teaching_group_name="АМБ-211",
            institute_name="Академия гражданской авиации",
            direction_code="25.03.03",
            direction_name="Аэронавигация",
            direction_level="бакалавриат",
            profile="Организация бизнес-процессов",
            form="очная",
            external_group_id=197175.0,
            course_from_file=2,
            external_permanent_group_id="309371",
        )
        assert row.external_group_id == "197175"
        assert row.code == "АМБ-2025-11"
        assert row.name == "АМБ-211"
        assert row.course_number == 2
        assert row.enrollment_year == 2025
        assert row.institute_code == "AGA"
        assert row.external_permanent_group_id == "309371"

    def test_build_group_import_row_applies_epo_override(self) -> None:
        row = build_group_import_row(
            permanent_group_code="ТУП-2025-11",
            teaching_group_name="ТУП-211",
            institute_name="Институт транспортной техники и систем управления",
            direction_code="38.03.03",
            direction_name="Управление персоналом",
            direction_level="бакалавриат",
            profile="Профиль",
            form="очная",
            external_group_id="149820",
            course_from_file=2,
        )
        assert row.name == "ЭПО-211"
        assert row.institute_code == "IEF"
        assert row.external_group_id == "149820"

    def test_build_rejects_remapped_away_id(self) -> None:
        with pytest.raises(ValueError, match="слит"):
            build_group_import_row(
                permanent_group_code="ТСТ-2023-42",
                teaching_group_name="ТСТ-442",
                institute_name="Институт управления и цифровых технологий",
                direction_code="09.03.01",
                direction_name="Информатика",
                direction_level="бакалавриат",
                profile="",
                form="очная",
                external_group_id="193902",
                course_from_file=4,
            )

    def test_remap_external_group_id_tst_442_to_441(self) -> None:
        assert remap_external_group_id(193902) == "193901"
        assert remap_external_group_id("193902.0") == "193901"
        assert remap_external_group_id(193901) == "193901"

    def test_normalize_external_group_id(self) -> None:
        assert normalize_external_group_id(149820.0) == "149820"
        assert normalize_external_group_id("") == ""

    def test_claim_by_external_id(self) -> None:
        candidates = [
            ExistingGroupCandidate(
                pk=1, code="АМБ-2025-11", name="АМБ-211", external_group_id="197175"
            )
        ]
        claimed = resolve_existing_group_for_id(
            candidates,
            external_id="197175",
            permanent_code="АМБ-2025-11",
            teaching_name="АМБ-211",
            ids_per_permanent={"АМБ-2025-11": {"197175"}},
            claimed_pks=set(),
        )
        assert claimed is not None
        assert claimed.pk == 1

    def test_claim_by_name_on_split(self) -> None:
        candidates = [
            ExistingGroupCandidate(
                pk=10, code="ТКИ-2024-41", name="ТКИ-341", external_group_id=""
            )
        ]
        ids = {"ТКИ-2024-41": {"193722", "193714"}}
        claimed_341 = resolve_existing_group_for_id(
            candidates,
            external_id="193714",
            permanent_code="ТКИ-2024-41",
            teaching_name="ТКИ-341",
            ids_per_permanent=ids,
            claimed_pks=set(),
        )
        assert claimed_341 is not None
        assert claimed_341.pk == 10

        claimed_241 = resolve_existing_group_for_id(
            candidates,
            external_id="193722",
            permanent_code="ТКИ-2024-41",
            teaching_name="ТКИ-241",
            ids_per_permanent=ids,
            claimed_pks={10},
        )
        assert claimed_241 is None

    def test_claim_single_id_for_permanent(self) -> None:
        candidates = [
            ExistingGroupCandidate(
                pk=5, code="АМБ-2025-11", name="Старое", external_group_id=""
            )
        ]
        claimed = resolve_existing_group_for_id(
            candidates,
            external_id="197175",
            permanent_code="АМБ-2025-11",
            teaching_name="АМБ-211",
            ids_per_permanent={"АМБ-2025-11": {"197175"}},
            claimed_pks=set(),
        )
        assert claimed is not None
        assert claimed.pk == 5

    def test_is_skipped_permanent_group_by_prefix(self) -> None:
        assert is_skipped_permanent_group("ТУП-2024-11")
        assert not is_skipped_permanent_group("ТПВг-2024-41")

    def test_is_skipped_study_group_name(self) -> None:
        assert is_skipped_study_group_name("ОММ-221")
        assert not is_skipped_study_group_name("АМБ-211")

    def test_collect_teaching_group_names_in_file(self) -> None:
        names = collect_teaching_group_names_in_file(
            ["ТКИ-241", "ТКИ-341", "", None, "ОММ-221"]
        )
        assert names == {"ТКИ-241", "ТКИ-341"}

    def test_map_teaching_group_name_abbrev_rename(self) -> None:
        assert map_teaching_group_name_for_lookup("ЭБП-311") == "ЭПТ-311"

    def test_resolve_study_group_display_name_by_code(self, monkeypatch) -> None:
        monkeypatch.setattr(
            "teams.domain.study_group_import.STUDY_GROUP_NAME_OVERRIDES_BY_CODE",
            {"АМБ-2025-11": "АМБ-211Н"},
        )
        assert (
            resolve_study_group_display_name(
                calculated_name="АМБ-211",
                permanent_group_code="АМБ-2025-11",
            )
            == "АМБ-211Н"
        )

    def test_get_study_group_override_known_ids(self) -> None:
        override = get_study_group_override_by_external_id(140100)
        assert override is not None
        assert override.name == "ЭПО-311"
