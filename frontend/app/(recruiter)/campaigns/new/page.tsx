"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowLeft, Plus, Trash2 } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useFieldArray, useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

import { Field } from "@/components/forms/field";
import { FadeIn } from "@/components/motion/motion";
import { Button, buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { ApiError } from "@/lib/api-client";
import { authStore } from "@/lib/auth-store";
import { cn } from "@/lib/utils";
import { CampaignService } from "@/services/campaign-service";

// Client-side schema for responsive UX only — the backend re-validates and remains
// the source of truth (it owns the real rules and any it adds later).
const schema = z.object({
  role_title: z.string().trim().min(1, "Role title is required").max(255),
  bar: z.string().trim().min(1, "Describe the bar a candidate must clear").max(500),
  competencies: z
    .array(z.object({ name: z.string().max(120), description: z.string().max(500) }))
    .refine((rows) => rows.some((r) => r.name.trim().length > 0), {
      message: "Add at least one competency",
    }),
});
type FormValues = z.infer<typeof schema>;

export default function NewCampaignPage() {
  const router = useRouter();
  useEffect(() => {
    if (!authStore.getAccess()) router.replace("/login");
  }, [router]);

  const {
    register,
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { role_title: "", bar: "", competencies: [{ name: "", description: "" }] },
  });
  const { fields, append, remove } = useFieldArray({ control, name: "competencies" });

  async function onSubmit(values: FormValues) {
    const named = values.competencies.filter((c) => c.name.trim());
    try {
      const res = await CampaignService.create({
        role_title: values.role_title.trim(),
        role_profile: {
          bar: values.bar.trim(),
          competencies: named.map((c) => ({
            name: c.name.trim(),
            description: c.description.trim() || null,
          })),
        },
      });
      toast.success("Campaign created");
      router.push(`/campaigns/${res.data.id}`);
    } catch (err: unknown) {
      if (err instanceof ApiError && err.status === 401) {
        router.replace("/login");
        return;
      }
      // Surface the backend's verdict verbatim — we don't second-guess it.
      toast.error(err instanceof Error ? err.message : "Could not create campaign");
    }
  }

  return (
    <FadeIn className="mx-auto max-w-2xl space-y-6">
      <div>
        <Link
          href="/campaigns"
          className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1 text-sm transition-colors lg:hidden"
        >
          <ArrowLeft className="size-4" aria-hidden />
          Campaigns
        </Link>
        <h1 className="mt-3 text-2xl font-semibold tracking-tight">New campaign</h1>
        <p className="text-muted-foreground text-sm">
          Define the role and how candidates are evaluated. You can review it before activating.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6" noValidate>
        <Card>
          <CardContent className="space-y-5 pt-6">
            <Field
              label="Role title"
              htmlFor="role_title"
              hint="Who you're hiring."
              error={errors.role_title?.message}
            >
              <Input
                id="role_title"
                placeholder="e.g. Senior Data Engineer"
                {...register("role_title")}
              />
            </Field>
            <Field
              label="Hiring bar"
              htmlFor="bar"
              hint="What strong evidence should demonstrate — the standard a candidate must clear, in your words."
              error={errors.bar?.message}
            >
              <Textarea
                id="bar"
                placeholder="e.g. Ships correct, well-tested SQL independently…"
                {...register("bar")}
              />
            </Field>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex-row items-center justify-between">
            <div className="space-y-1">
              <CardTitle className="text-base">Competencies</CardTitle>
              <CardDescription>
                The capabilities that matter for this role. Next, you&apos;ll design work-sample
                tasks that let candidates show evidence for each.
              </CardDescription>
            </div>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => append({ name: "", description: "" })}
            >
              <Plus className="size-4" aria-hidden />
              Add
            </Button>
          </CardHeader>
          <CardContent className="space-y-3">
            {fields.map((f, i) => (
              <div key={f.id} className="flex items-start gap-2 rounded-lg border p-3">
                <div className="flex-1 space-y-2">
                  <Input placeholder="Competency (e.g. SQL)" {...register(`competencies.${i}.name`)} />
                  <Input
                    placeholder="Description (optional)"
                    {...register(`competencies.${i}.description`)}
                  />
                </div>
                {fields.length > 1 && (
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    aria-label="Remove competency"
                    onClick={() => remove(i)}
                  >
                    <Trash2 className="size-4" aria-hidden />
                  </Button>
                )}
              </div>
            ))}
            {(errors.competencies?.root?.message ?? errors.competencies?.message) && (
              <p className="text-destructive text-xs">
                {errors.competencies?.root?.message ?? errors.competencies?.message}
              </p>
            )}
          </CardContent>
        </Card>

        <div className="flex justify-end gap-2">
          <Link href="/campaigns" className={cn(buttonVariants({ variant: "ghost" }))}>
            Cancel
          </Link>
          <Button type="submit" loading={isSubmitting}>
            Create campaign
          </Button>
        </div>
      </form>
    </FadeIn>
  );
}
