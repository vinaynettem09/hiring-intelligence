"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import type { ReactNode } from "react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

import { Field } from "@/components/forms/field";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { CandidateService } from "@/services/candidate-service";

const schema = z.object({
  name: z.string().trim().min(1, "Name is required"),
  email: z.string().email("Enter a valid email"),
});
type FormValues = z.infer<typeof schema>;

export function AddCandidateDialog({
  campaignId,
  onAdded,
  trigger,
}: {
  campaignId: string;
  onAdded: () => void;
  trigger: ReactNode;
}) {
  const [open, setOpen] = useState(false);
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: "", email: "" },
  });

  async function onSubmit(values: FormValues) {
    try {
      await CandidateService.add(campaignId, values);
      toast.success("Candidate added");
      reset();
      setOpen(false);
      onAdded();
    } catch (err: unknown) {
      // Surface the backend's verdict (e.g. CANDIDATE_ALREADY_IN_CAMPAIGN).
      toast.error(err instanceof Error ? err.message : "Could not add candidate");
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add candidate</DialogTitle>
          <DialogDescription>
            They will be invited to complete this campaign’s work sample.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
          <Field label="Full name" htmlFor="candidate-name" error={errors.name?.message}>
            <Input id="candidate-name" placeholder="Ada Lovelace" {...register("name")} />
          </Field>
          <Field label="Email" htmlFor="candidate-email" error={errors.email?.message}>
            <Input
              id="candidate-email"
              type="email"
              placeholder="ada@company.com"
              {...register("email")}
            />
          </Field>
          <div className="flex justify-end">
            <Button type="submit" loading={isSubmitting}>
              Add candidate
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
