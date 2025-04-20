from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property
from taggit.models import TaggedItem
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.admin.views.generic import IndexView

from wagtail_tagmanager.models import ManagedTag
from wagtail_tagmanager.utils import get_base_page_model, get_page_tagging_model
from wagtail_tagmanager.viewsets import ManagedTagViewSet


class ManageTaggedObjectsView(IndexView):
    template_name = "wagtail_tagmanager/manage_tagged_objects.html"
    page_title = "Pages using tag"
    paginate_by = 15

    @cached_property
    def page_tag_model(self):
        return get_page_tagging_model()

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        if action == "remove_tag":
            selected_items = request.POST.getlist("selected_items")
            if selected_items:
                object_ids = [int(object_id) for object_id in selected_items]

                # Remove from page tag model
                self.page_tag_model.objects.filter(
                    tag=self.tag, content_object_id__in=object_ids
                ).delete()

                # Remove from all other tagged items
                TaggedItem.objects.filter(
                    tag=self.tag, object_id__in=object_ids
                ).delete()

                messages.success(
                    request,
                    f"Removed tag '{self.tag.name}' from {len(object_ids)} pages.",
                )

        return HttpResponseRedirect(request.get_full_path())

    def dispatch(self, request, *args, **kwargs):
        self.tag = get_object_or_404(ManagedTag, id=self.kwargs["tag_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        objects = self.tag.get_tagged_objects()

        search_query = self.request.GET.get("q", "").strip().lower()

        if search_query:

            def match(obj):
                for attr in ("title", "name"):
                    value = getattr(obj, attr, None)
                    if isinstance(value, str) and search_query in value.lower():
                        return True
                return search_query in str(obj).lower()

            objects = [obj for obj in objects if match(obj)]

        return objects

    def get_admin_edit_url(self, obj):
        return AdminURLFinder(self.request.user).get_edit_url(obj)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viewset = ManagedTagViewSet()
        context["edit_url"] = reverse(viewset.get_url_name("edit"), args=[self.tag.pk])
        context["tag"] = self.tag
        context["can_add_pages"] = bool(
            getattr(settings, "WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL", None)
        )
        context["object_list"] = [
            {
                "obj": obj,
                "model_name": obj._meta.verbose_name.title(),
                "edit_url": self.get_admin_edit_url(obj),
            }
            for obj in context["object_list"]
        ]

        return context


class AddPagesToTagView(IndexView):
    template_name = "wagtail_tagmanager/add_pages_to_tag.html"
    paginate_by = 15

    @cached_property
    def page_tag_model(self):
        return get_page_tagging_model()

    @cached_property
    def base_page_model(self):
        return get_base_page_model()

    def dispatch(self, request, *args, **kwargs):
        self.tag = get_object_or_404(ManagedTag, id=self.kwargs["tag_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        tagged_page_ids = self.page_tag_model.objects.filter(tag=self.tag).values_list(
            "content_object_id", flat=True
        )
        pages = (
            self.base_page_model.objects.exclude(id__in=tagged_page_ids)
            .live()
            .specific()
        )
        search_query = self.request.GET.get("q", None)

        if search_query:
            pages = pages.filter(title__icontains=search_query)

        return pages

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context

    def post(self, request, *args, **kwargs):
        selected_items = request.POST.getlist("selected_items")
        if selected_items:
            page_ids = [int(i) for i in selected_items]
            pages = self.base_page_model.objects.filter(id__in=page_ids).specific()

            for page in pages:
                self.page_tag_model.objects.get_or_create(
                    content_object=page, tag=self.tag
                )

            messages.success(
                request, f"Tag '{self.tag.name}' added to {len(pages)} pages."
            )

        return HttpResponseRedirect(
            reverse("wagtail_tagmanager_manage_objects", args=[self.tag.id])
        )
