"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

import { Field } from "@/components/forms/field";
import { AuthShell } from "@/components/layout/auth-shell";
import { FadeIn } from "@/components/motion/motion";
import { Button, buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { IdentityService } from "@/services/identity-service";
import type { SignupResponse } from "@/types/identity";

const schema = z.object({
  organization_name: z.string().trim().min(1, "Organization name is required"),
  email: z.string().email("Enter a valid work email"),
  password: z.string().min(8, "At least 8 characters"),
});
type FormValues = z.infer<typeof schema>;

export default function SignupPage() {
  const [created, setCreated] = useState<SignupResponse | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { organization_name: "", email: "", password: "" },
  });

  async function onSubmit(values: FormValues) {
    try {
      const res = await IdentityService.signup(values);
      setCreated(res.data);
      toast.success("Account created");
    } catch (err: unknown) {
      toast.error(err instanceof Error ? err.message : "Signup failed");
    }
  }

  return (
    <AuthShell>
      <FadeIn>
        {created ? (
          <Card className="shadow-elevated">
            <CardHeader>
              <CardTitle>You’re all set</CardTitle>
              <CardDescription>
                <strong>{created.organization.name}</strong> is ready, and {created.user.email} is
                its admin.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/login" className={cn(buttonVariants(), "w-full")}>
                Continue to log in
              </Link>
            </CardContent>
          </Card>
        ) : (
          <Card className="shadow-elevated">
            <CardHeader>
              <CardTitle>Create your account</CardTitle>
              <CardDescription>Set up your organization to get started.</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
                <Field
                  label="Organization name"
                  htmlFor="org"
                  error={errors.organization_name?.message}
                >
                  <Input id="org" placeholder="Acme Inc" {...register("organization_name")} />
                </Field>
                <Field label="Work email" htmlFor="email" error={errors.email?.message}>
                  <Input
                    id="email"
                    type="email"
                    autoComplete="email"
                    placeholder="you@company.com"
                    {...register("email")}
                  />
                </Field>
                <Field
                  label="Password"
                  htmlFor="password"
                  hint="At least 8 characters."
                  error={errors.password?.message}
                >
                  <Input
                    id="password"
                    type="password"
                    autoComplete="new-password"
                    {...register("password")}
                  />
                </Field>
                <Button type="submit" className="w-full" loading={isSubmitting}>
                  Create account
                </Button>
              </form>
              <p className="text-muted-foreground mt-4 text-center text-sm">
                Already have an account?{" "}
                <Link href="/login" className="text-primary font-medium hover:underline">
                  Log in
                </Link>
              </p>
            </CardContent>
          </Card>
        )}
      </FadeIn>
    </AuthShell>
  );
}
