from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import YES
from edc_lab_panel.panels import hba1c_panel
from edc_metadata.metadata_rules import PredicateCollection
from edc_visit_schedule.constants import DAY1, MONTH1, MONTH3, MONTH6, WEEK2
from edc_visit_schedule.utils import is_baseline


def hba1c_crf_required_at_baseline(visit):
    model_name = "meta_subject.bloodresultshba1c"
    screening_model_cls = django_apps.get_model("meta_screening.subjectscreening")
    bloodresults_model_cls = django_apps.get_model(model_name)
    required = False
    if is_baseline(visit):
        try:
            screening_model_cls.objects.get(
                subject_identifier=visit.subject_identifier,
                hba1c_value__isnull=True,
            )
        except ObjectDoesNotExist:
            pass
        else:
            try:
                obj = bloodresults_model_cls.objects.get(
                    subject_visit__visit_code=DAY1,
                    subject_visit__visit_code_sequence=0,
                )
            except ObjectDoesNotExist:
                required = True
            else:
                if not obj.hba1c_value:
                    required = True
    return required


def hba1c_requisition_required_at_baseline(visit):
    screening_model_cls = django_apps.get_model("meta_screening.subjectscreening")
    required = False
    if is_baseline(visit):
        try:
            screening_model_cls.objects.get(
                subject_identifier=visit.subject_identifier,
                hba1c_value__isnull=False,
            )
        except ObjectDoesNotExist:
            required = True
    return required


class Predicates(PredicateCollection):

    app_label = "meta_subject"
    visit_model = "meta_subject.subjectvisit"

    @staticmethod
    def hba1c_crf_required(visit, **kwargs) -> bool:
        """Require at baseline visit if not recorded on the
        screening form.
        """
        required = hba1c_crf_required_at_baseline(visit)
        if (
            not required
            and visit.appointment.visit_code != DAY1
            and visit.appointment.visit_code_sequence == 0
            and visit.appointment.visit_code
            in visit.schedule.crf_required_at("meta_subject.bloodresultshba1c")
        ):
            required = True
        return required

    @staticmethod
    def hba1c_requisition_required(visit, **kwargs) -> bool:
        """Require at baseline visit if not recorded on the
        screening form.
        """
        required = hba1c_requisition_required_at_baseline(visit)
        if (
            not required
            and visit.appointment.visit_code != DAY1
            and visit.appointment.visit_code_sequence == 0
            and visit.appointment.visit_code
            in visit.schedule.requisition_required_at(hba1c_panel)
        ):
            required = True
        return required

    def health_economics_required(self, visit, **kwargs) -> bool:
        """Returns true if HE was not completed at week 2"""

        required = False
        if (
            visit.appointment.visit_code == WEEK2
            and visit.appointment.visit_code_sequence == 0
        ):
            required = True
        elif (
            visit.appointment.visit_code == MONTH1
            and visit.appointment.visit_code_sequence == 0
        ):

            model_cls = django_apps.get_model(f"{self.app_label}.healtheconomicssimple")
            try:
                model_cls.objects.get(
                    subject_visit__subject_identifier=visit.subject_identifier,
                    subject_visit__visit_code=WEEK2,
                    subject_visit__visit_code_sequence=0,
                )
            except ObjectDoesNotExist:
                required = True
        return required

    def hepatitis_test_required(self, visit, **kwargs) -> bool:
        """Returns True if required.

        Bu default is required at baseline. If not then at week2 or 1 month"""
        model_cls = django_apps.get_model(f"{self.app_label}.hepatitistest")
        hcv_performed = False
        hbsag_performed = False
        required = True
        for visit_code in [DAY1, WEEK2, MONTH1]:
            try:
                obj = model_cls.objects.get(
                    subject_visit__subject_identifier=visit.subject_identifier,
                    subject_visit__visit_code=visit_code,
                    subject_visit__visit_code_sequence=0,
                )
            except ObjectDoesNotExist:
                pass
            else:
                if not hbsag_performed:
                    hbsag_performed = obj.hbsag_performed == YES
                if not hcv_performed:
                    hcv_performed = obj.hcv_performed == YES
                if hbsag_performed and hcv_performed:
                    required = False
                    break
        return required

    def mnsi_required(self, visit, **kwargs) -> bool:
        """Returns True if MNSI assessment was not performed at the
        1M, 3M or 6M visits.
        """
        required = True
        if (
            visit.appointment.visit_code in [MONTH1, MONTH3, MONTH6]
        ) and visit.appointment.visit_code_sequence == 0:
            model_cls = django_apps.get_model(f"{self.app_label}.mnsi")
            objs = model_cls.objects.filter(
                subject_visit__subject_identifier=visit.subject_identifier,
                subject_visit__visit_code__in=[MONTH1, MONTH3, MONTH6],
                subject_visit__visit_code_sequence=0,
            )
            for obj in objs:
                if obj.mnsi_performed == YES:
                    required = False
                    break
        return required
